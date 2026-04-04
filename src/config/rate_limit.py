from fastapi import Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from src.infrastructure.security.auth_service import decode_access_token

def get_user_id_or_ip(request: Request) -> str:
    """
    Kullanıcı giriş yapmışsa (JWT Token varsa) işlemi User ID üzerinden kısıtlar.
    Giriş yapmamışsa (Kayıt ol/Giriş ekranı vb.) IP adresi üzerinden kısıtlar.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = decode_access_token(token)
        # Eğer token geçerliyse ve içinde kullanıcı ID'si ('sub') varsa
        if payload and "sub" in payload:
            return f"user:{payload['sub']}"
            
    # Token yoksa veya geçersizse mecburen IP adresine (NAT) düşeriz
    return f"ip:{get_remote_address(request)}"

# Global limiter instance
limiter = Limiter(
    key_func=get_user_id_or_ip,
    default_limits=["100/minute"]
)
