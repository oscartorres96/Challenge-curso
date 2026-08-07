from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.notifications import NotificationCreate, NotificationsResponse, NotificationsDelete
from app.services.notification_service import NotificationService
from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    dependencies=[Depends(get_current_user)]
)


@router.post(
    "",
    response_model=NotificationsResponse,
    status_code=status.HTTP_201_CREATED
)
def create_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db)
):
    return NotificationService.create_notification(
        db=db,
        notification_data=notification_data
    )


@router.get(
    "/{user_id}",
    response_model=list[NotificationsResponse],
    status_code=status.HTTP_200_OK
)
def get_notification(
    user_id: int,
    db: Session = Depends(get_db)
):
    return NotificationService.get_notifications_by_user(
        user_id=user_id,
        db=db
    )


@router.get(
    "",
    response_model=list[NotificationsResponse],
    status_code=status.HTTP_200_OK
)
def get_all_notifications(
    db: Session = Depends(get_db)
):
    return NotificationService.get_all_notifications(
        db=db
    )


@router.put(
    "/{notification_id}",
    response_model=NotificationsResponse,
    status_code=status.HTTP_200_OK
)
def update_notification(
    notification_id: int,
    notification_data: NotificationsDelete,
    db: Session = Depends(get_db)
):
    return NotificationService.update_notification(
        notification_id=notification_id,
        notification_data=notification_data,
        db=db
    )


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    return NotificationService.delete_notification(
        notification_id=notification_id,
        db=db
    )
