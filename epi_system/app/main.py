import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.api.routes import audit, colaboradores, epis, lgpd, retiradas
from app.audit.listeners import register_audit_listeners
from app.core.config import get_settings
from app.core.database import Base, engine
from app.services.scheduler import build_scheduler

settings = get_settings()
register_audit_listeners()

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Erro interno"})


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(status_code=429, content={"detail": "Muitas requisições"})


app.include_router(epis.router)
app.include_router(colaboradores.router)
app.include_router(retiradas.router)
app.include_router(audit.router)
app.include_router(lgpd.router)

scheduler = build_scheduler()


@app.on_event("startup")
def startup() -> None:
    if settings.auto_create_tables:
        Base.metadata.create_all(bind=engine)
    if os.getenv("VERCEL"):
        return
    if not scheduler.running:
        scheduler.start()


@app.on_event("shutdown")
def shutdown() -> None:
    if os.getenv("VERCEL"):
        return
    if scheduler.running:
        scheduler.shutdown(wait=False)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/privacidade", tags=["lgpd"])
def privacidade_publica() -> dict[str, object]:
    return lgpd.privacidade()
