import uuid
from logging.config import dictConfig
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, status
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import sentry_sdk
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from src.config.settings import settings

# Initialize Sentry
if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of transactions.
        profiles_sample_rate=1.0,
        send_default_pii=True,
    )

# Import routers
from src.presentation.api.v1.routers import (
    ingredients,
    recipes,
    user_router,
    social_router,
)
from src.adapters.database.postgresql.database import get_db
from src.config.logging import get_logging_config
from src.domain.exceptions import RecipeAppError, ConflictError, AlreadyExistsError
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from src.config.rate_limit import limiter, _rate_limit_exceeded_handler

DEFAULT_RESPONSE_CLASS = ORJSONResponse

# Configure logging
log_config = get_logging_config(
    log_level="INFO",
    is_enabled=True,
)
dictConfig(log_config)

# Get a logger instance
log = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Application starting up and checking DB connection...")
    try:
        async for session in get_db():
            await session.execute(text("SELECT 1"))
            log.info("Database connection successful.")
            break
    except Exception as e:
        log.error("Database connection failed", exc_info=True)
        raise e
        
    yield
    
    log.info("Application shutting down...")


app = FastAPI(
    title="Recipe AI API",
    description="Clean Architecture based Recipe API",
    version="1.0.0",
    lifespan=lifespan,
    default_response_class=DEFAULT_RESPONSE_CLASS,
)

# GZIP Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

# Rate Limiter
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# --- CORS ---
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
]

# Add external origins from settings
if settings.allowed_origins:
    origins.extend(settings.allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Logging Middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    structlog.contextvars.clear_contextvars()

    request_id = str(uuid.uuid4())
    client_ip = request.client.host if request.client else "unknown"
    structlog.contextvars.bind_contextvars(
        trace={"id": request_id},
        client={"ip": client_ip},
        http={
            "request": {
                "id": request_id,
                "method": request.method,
                "path": request.url.path,
            }
        },
    )
    log.info("Request received")

    response = await call_next(request)

    structlog.contextvars.bind_contextvars(
        http={
            "request": {
                "id": request_id,
                "method": request.method,
                "path": request.url.path,
            },
            "response": {"status_code": response.status_code},
        }
    )
    log.info("Request completed")
    return response


# --- Exception Handlers ---
@app.exception_handler(RecipeAppError)
async def recipe_app_error_handler(request: Request, exc: RecipeAppError):
    headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None
    
    return DEFAULT_RESPONSE_CLASS(
        status_code=exc.status_code,
        content=exc.to_dict(),
        headers=headers
    )

@app.exception_handler(IntegrityError)
async def sqlalchemy_integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Catch Database level errors (Foreign Key violations, Unique constraints)
    and map them to human-friendly domain errors.
    """
    detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
    # 1. Foreign Key Constraint (In-use error)
    if "is still referenced from table" in detail or "violates foreign key constraint" in detail:
        # Example message parsing can be improved, but this is the core logic
        error = ConflictError(
            message="Bu öğeyi silemezsiniz çünkü başka kayıtlar (örneğin tarifler) bu öğeye bağlı."
        )
        return await recipe_app_error_handler(request, error)

    # 2. Unique Constraint (Already exists error)
    if "already exists" in detail or "duplicate key" in detail:
        error = AlreadyExistsError(
            message="Bu kayıt zaten mevcut. Lütfen farklı bir isim veya e-posta deneyin."
        )
        return await recipe_app_error_handler(request, error)

    # Fallback to general DB error
    log.error("Unhandled Database Integrity Error", detail=detail, exc_info=True)
    return DEFAULT_RESPONSE_CLASS(
        status_code=400,
        content={
            "code": "DATABASE_ERROR",
            "message": "Veritabanı işlemi sırasında bir çakışma oluştu. Lütfen verileri kontrol edin."
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return DEFAULT_RESPONSE_CLASS(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)},
    )

@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return DEFAULT_RESPONSE_CLASS(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"error": "Too Many Requests", "detail": f"Rate limit exceeded: {exc.detail}"}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    log.error("Unhandled exception", exc_info=True)
    return DEFAULT_RESPONSE_CLASS(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "errorCode": 500,
            "errorMessage": "Internal Server Error"
        },
    )


# --- Routers ---
app.include_router(ingredients.router, prefix="/api/v1/ingredients", tags=["Ingredients"])
app.include_router(recipes.router, prefix="/api/v1/recipes", tags=["Recipes"])
app.include_router(user_router.router, prefix="/api/v1", tags=["Users"])
app.include_router(social_router.router, prefix="/api/v1", tags=["Social"])


@app.get("/")
async def root():
    return {"message": "Welcome to Recipe AI API"}


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
