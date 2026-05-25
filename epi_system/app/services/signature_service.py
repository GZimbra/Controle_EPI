import uuid
from pathlib import Path

from app.core.config import get_settings
from app.core.security import decode_base64_payload, get_fernet, sha256_hex


def save_encrypted_signature(assinatura_base64: str) -> tuple[str, str]:
    raw = decode_base64_payload(assinatura_base64)
    digest = sha256_hex(raw)
    encrypted = get_fernet().encrypt(raw)
    storage = Path(get_settings().signature_storage_dir)
    storage.mkdir(parents=True, exist_ok=True)
    path = storage / f"{uuid.uuid4().hex}.sig.enc"
    path.write_bytes(encrypted)
    return digest, str(path)
