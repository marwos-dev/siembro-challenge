import logging
import sys

LOG_FORMAT = (
    "[%(asctime)s] [%(levelname)s] [%(name)s] "
    "%(message)s"
)


def configure_logging(debug: bool = False):
    """
    Configura logging global de la aplicación.
    - Logs en stdout (útil para Docker & Kubernetes)
    - Formato uniforme
    - Nivel DEBUG si está activado el modo debug
    """
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format=LOG_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Reducir verbosidad de librerías externas
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
