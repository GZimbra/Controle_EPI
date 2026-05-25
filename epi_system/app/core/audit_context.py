from contextvars import ContextVar


audit_user: ContextVar[str] = ContextVar("audit_user", default="system")
audit_ip: ContextVar[str] = ContextVar("audit_ip", default="local")


def set_audit_context(user: str, ip: str) -> None:
    audit_user.set(user or "system")
    audit_ip.set(ip or "local")
