import os

os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("FERNET_KEY", "9x2g48YLUTn4nraPGA0m9fMUfB0zR8c_I4Jwiu2ZtQg=")
os.environ.setdefault("CPF_PEPPER", "test-pepper")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.audit.listeners import register_audit_listeners
from app.core.database import Base
from app.models import AuditLog, Colaborador, EPI, RetiradaEPI, UsuarioSistema


@pytest.fixture()
def db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    register_audit_listeners()
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
