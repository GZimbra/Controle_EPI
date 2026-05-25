import base64
import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from cryptography.fernet import Fernet
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_fernet() -> Fernet:
    return Fernet(get_settings().fernet_key.encode())


def encrypt_text(value: str) -> str:
    return get_fernet().encrypt(value.encode()).decode()


def decrypt_text(token: str) -> str:
    return get_fernet().decrypt(token.encode()).decode()


def sha256_hex(data: bytes | str) -> str:
    raw = data.encode() if isinstance(data, str) else data
    return hashlib.sha256(raw).hexdigest()


def generate_salt() -> str:
    return secrets.token_hex(16)


def hash_cpf(cpf: str, salt: str) -> str:
    normalized = "".join(ch for ch in cpf if ch.isdigit())
    return sha256_hex(f"{normalized}:{salt}:{get_settings().cpf_pepper}")


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str, claims: dict[str, Any] | None = None) -> str:
    settings = get_settings()
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    if claims:
        payload.update(claims)
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, get_settings().secret_key, algorithms=[get_settings().jwt_algorithm])
    except JWTError as exc:
        raise ValueError("invalid_token") from exc


def decode_base64_payload(data_url_or_base64: str) -> bytes:
    payload = data_url_or_base64.split(",", 1)[1] if "," in data_url_or_base64 else data_url_or_base64
    return base64.b64decode(payload, validate=True)
