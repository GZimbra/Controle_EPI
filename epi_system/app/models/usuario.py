from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import TimestampMixin


class UsuarioSistema(TimestampMixin, Base):
    __tablename__ = "usuarios_sistema"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    matricula: Mapped[str | None] = mapped_column(String(50), nullable=True)
    role: Mapped[str] = mapped_column(String(40), nullable=False, default="operador")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
