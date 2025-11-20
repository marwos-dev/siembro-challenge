# app/tests/conftest.py
import os
import sys
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- 0) Asegurarnos de que el root del proyecto esté en sys.path ---
# Este archivo está en: <root>/app/tests/conftest.py
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.main import app
from app.db.session import Base, get_db
from app.db.models.user import User
from app.auth.dependencies import CurrentUser, get_current_user

TEST_DATABASE_URL = "sqlite:///./test_db.sqlite"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """
    Se ejecuta una vez por sesión de tests.
    Dropea y crea todas las tablas para asegurarnos
    de que users y notes existen.
    """
    # Si querés asegurarte que está limpio:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def db_session():
    """
    Sesión de DB por test.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# --- 2) Override de get_db de la app ---
def override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# Limpiamos overrides anteriores y registramos el nuevo get_db
app.dependency_overrides.clear()
app.dependency_overrides[get_db] = override_get_db


# --- 3) Mock de usuario autenticado / get_current_user ---
@pytest.fixture
def mock_user(db_session):
    """
    Crea un usuario con auth0_sub y email únicos por test,
    para evitar problemas con constraints UNIQUE.
    """
    unique_suffix = uuid.uuid4().hex[:8]
    auth0_sub = f"auth0|{unique_suffix}"
    email = f"test-{unique_suffix}@example.com"

    user = User(
        auth0_sub=auth0_sub,
        email=email,
        name="Test User",
        metadata_json={"last_login_at": "2025-01-01T10:00:00Z"},
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def override_get_current_user_fn(user: User):
    def _override():
        return CurrentUser(user=user, claims={"sub": user.auth0_sub})

    return _override


@pytest.fixture
def client(mock_user):
    """
    Cliente de test con el usuario autenticado mockeado.
    """
    # override de la dependencia real get_current_user
    app.dependency_overrides[get_current_user] =\
        override_get_current_user_fn(mock_user)
    return TestClient(app)
