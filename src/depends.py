from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService

user_repository = UserRepository()

user_service = UserService(user_repository)


def get_user_service() -> UserService:
    return user_service
