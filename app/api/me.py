from fastapi import APIRouter, Depends

from app.auth.dependencies import CurrentUser, get_current_user
from app.db.models.note import Note
from app.db.models.user import User
from app.db.session import Session, get_db
from app.schemas.user import MeOut

me_router = APIRouter()


@me_router.get("/", response_model=MeOut)
def get_me(
        current: CurrentUser = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return MeOut(
        sub=current.user.auth0_sub,
        email=current.user.email,
        name=current.user.name,
        metadata=dict(
            # Esto tambien se puede optimizar para ir actualizando la metadatada a medida
            # que vamos creando las notas
            count_notes=db.query(Note).filter(Note.user_id == current.user.id).count(),
            **current.user.metadata_json
        ),
    )
