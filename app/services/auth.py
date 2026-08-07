from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str,
    ) -> User | None:
        user = UserRepository.get_by_email(
            db=db,
            email=email,
        )

        if not user:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        return user