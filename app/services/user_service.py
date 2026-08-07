from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


class UserService:

    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        existing_user = UserRepository.get_by_email(
            db=db,
            email=user_data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists"
            )

        hashed_password = hash_password(user_data.password)

        return UserRepository.create(
            db=db,
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            phone_number=user_data.phone_number,
            device_token=user_data.device_token
        )

    @staticmethod
    def get_all_users(db: Session):
        return UserRepository.get_all(db=db)

    @staticmethod
    def delete_user(user_id: int, db: Session):
        return UserRepository.delete_user(
            user_id=user_id, 
            db=db
        )

    @staticmethod
    def update_user(
        user_id: int, 
        db: Session,
        user_data: UserUpdate
    ):
        update_data = user_data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided"
            )

        email = update_data.get("email")
        if email is not None:
            existing_user = UserRepository.get_by_email(
                db=db,
                email=email
            )

            if existing_user is not None and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A user with this email already exists"
                )

        return UserRepository.update_user(
            db=db,
            user_id=user_id,
            update_data=update_data
        )
