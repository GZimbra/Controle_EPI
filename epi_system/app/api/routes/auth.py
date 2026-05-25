from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.models.usuario import UsuarioSistema
from app.schemas.auth import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/login", response_model=Token)
@limiter.limit(get_settings().auth_rate_limit)
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    user = db.scalar(select(UsuarioSistema).where(UsuarioSistema.username == payload.username, UsuarioSistema.is_active.is_(True)))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return Token(access_token=create_access_token(user.username, {"role": user.role}))
