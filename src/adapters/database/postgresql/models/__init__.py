# Base and Model Registry
# All models must be imported here so Alembic can find them in Base.metadata

from .base import Base
from .ingredient import IngredientModel
from .recipe import RecipeModel, RecipeIngredientModel, RecipeStatus
from .user import UserModel
from .profile import UserProfileModel
from .tag import TagModel, RecipeTagModel
from .instruction import InstructionStepModel
from .equipment import EquipmentModel, RecipeEquipmentModel
from .social import CommentModel, ReviewModel, FollowModel, BlockModel, ReportModel, RecipeLikeModel
from .collection import CollectionModel, CollectionRecipeModel, MealPlanModel
from .gamification import CookLogModel, LevelModel, BadgeModel, UserBadgeModel
from .logs import SearchLogModel, ModerationLogModel

__all__ = [
    "Base",
    "IngredientModel",
    "RecipeModel",
    "RecipeIngredientModel",
    "RecipeStatus",
    "UserModel",
    "UserProfileModel",
    "TagModel",
    "RecipeTagModel",
    "InstructionStepModel",
    "EquipmentModel",
    "RecipeEquipmentModel",
    "CommentModel",
    "ReviewModel",
    "FollowModel",
    "BlockModel",
    "ReportModel",
    "RecipeLikeModel",
    "CollectionModel",
    "CollectionRecipeModel",
    "MealPlanModel",
    "CookLogModel",
    "LevelModel",
    "BadgeModel",
    "UserBadgeModel",
    "SearchLogModel",
    "ModerationLogModel"
]
