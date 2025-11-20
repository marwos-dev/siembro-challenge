from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    metadata_json = Column("metadata", JSON, nullable=True)

    # Esto nos ayudara a hacer una busqueda mas rapido creando un indice sobre la columna auth0_sub
    auth0_sub = Column(String(100), unique=True, nullable=False, index=True)

    # Relaciones
    notes = relationship("Note", back_populates="user")

    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False,
    )
