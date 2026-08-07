from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserList, UserUpdate
from app.services.user_service import UserService
from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)]
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    return UserService.create_user(
        db=db, 
        user_data=user_data
    )


@router.get(
    "",
    response_model=list[UserList],
    status_code=status.HTTP_200_OK
)
def get_users(
    db: Session = Depends(get_db)
):
    return UserService.get_all_users(db=db)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return UserService.delete_user(
        user_id=user_id, 
        db=db
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    return UserService.update_user(
        user_id=user_id,
        user_data=user_data,
        db=db
    )
