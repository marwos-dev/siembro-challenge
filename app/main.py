from fastapi import FastAPI

from app.api import health_router, me_router, note_router
from app.core.logging import configure_logging
from app.core.settings import settings

configure_logging(debug=settings.DEBUG)


# Configuración de la app
def get_application() -> FastAPI:
    app = FastAPI(
        title="siembro-user-notes-service",
        description="TEST",
        version="1.0.0",
        docs_url="/docs",
    )

    # Incluir routers
    include_routers(app)
    return app


# Inclusión modular de rutas
def include_routers(app: FastAPI) -> None:
    app.include_router(health_router, prefix="/health", tags=["Health"])
    app.include_router(me_router, prefix="/me", tags=["Me"])
    app.include_router(note_router, prefix="/notes", tags=["Notes"])


# Inicializa la app
app = get_application()
