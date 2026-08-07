from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base
from app.dependencies.database import get_db
from app.main import app
from app.core.security import create_access_token, hash_password
from app.models.user import User
from app.models.notification import Notification



@pytest.fixture()
def db_session(tmp_path) -> Generator[Session, None, None]:
    """
    Crea una base de datos SQLite temporal para cada test.
    tmp_path es proporcionado automáticamente por el pytest.
    """
    database_path = tmp_path / "test.db"
    database_url = f"sqlite:///{database_path}"

    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False}
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Hace que los endpoints utilicen la sesión de prueba
    en lugar de la base configurada en .env.
    """
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def test_password():
    return "password123"


@pytest.fixture()
def test_user(
    db_session: Session,
    test_password: str
) -> User:
    user = User(
        name="Usuario de prueba",
        email="test@example.com",
        phone_number="55512345678",
        device_token="test-device-token",
        hashed_password=hash_password(test_password)
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture()
def access_token(test_user: User) -> str:
    return create_access_token(subject=test_user.id)


@pytest.fixture()
def auth_header(access_token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {access_token}"
    }


@pytest.fixture()
def test_notification(
    db_session: Session,
    test_user: User
) -> Notification:
    notification = Notification(
        title="Test Notification",
        content="Original Content",
        channel="email",
        user_id=test_user.id,
    )

    db_session.add(notification)
    db_session.commit()
    db_session.refresh(notification)

    return notification
