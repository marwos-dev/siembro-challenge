from app.db.session import engine, Base
from .models.user import User  # importa para que SQLAlchemy registre el modelo
from .models.note import Note  # idem


def init_db() -> None:
    """
    Crea las tablas en la base si no existen.
    Solo para desarrollo / entorno de prueba del challenge.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()