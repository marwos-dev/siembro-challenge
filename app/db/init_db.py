from app.db.session import Base, engine


def init_db() -> None:
    """
    Crea las tablas en la base si no existen.
    Solo para desarrollo / entorno de prueba del challenge.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
