from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.delivery import Delivery
from app.models.notification import Notification
from app.models.user import User
from app.routers.users import router as users_router
from app.routers.notifications import router as notifications_router
from app.routers.deliveries import router as deliveries_router
from app.routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notifications API",
    version="1.0.0"
)

app.include_router(users_router)
app.include_router(notifications_router)
app.include_router(deliveries_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Notifications API is running."}
