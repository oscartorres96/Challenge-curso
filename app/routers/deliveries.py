from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.delivery import DeliveryResponse
from app.services.delivery_service import DeliveryService
from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"],
    dependencies=[Depends(get_current_user)]
)


@router.get(
    "",
    response_model=list[DeliveryResponse],
    status_code=status.HTTP_200_OK
)
def get_all_deliveries(
    db: Session = Depends(get_db)
):
    return DeliveryService.get_all_deliveries(
        db=db    
    )
