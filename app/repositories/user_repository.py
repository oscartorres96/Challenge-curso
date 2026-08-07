from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository: 

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int
    ):  
        user = db.get(User, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not found."
            )

        return user

    @staticmethod
    def create(
        db: Session,
        name: str,
        email: str,
        hashed_password: str,
        phone_number: str | None = None,
        device_token: str | None = None
    ) -> User:
        user = User(
            name=name,
            email=email,
            phone_number=phone_number,
            device_token=device_token,
            hashed_password=hashed_password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_all(
        db: Session
    ):
        return db.query(User).all()

    @staticmethod
    def delete_user(
        user_id: id,
        db: Session   
    ):
        user = db.get(User, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User has not fund."
            )

        db.delete(user)
        db.commit()

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        update_data: dict
    ) -> User:
        user = db.get(User, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)

        return user
