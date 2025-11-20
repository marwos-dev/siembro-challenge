from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import CurrentUser, get_current_user
from app.db.models.note import Note
from app.db.session import get_db
from app.schemas.note import NoteCreate, NoteOut

note_router = APIRouter()


@note_router.get("/", response_model=List[NoteOut])
async def list_notes(
        current: CurrentUser = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return db.query(Note).filter(
        Note.user_id == current.user.id
    ).order_by(Note.created_at.desc()).all()


@note_router.post("/", response_model=NoteOut)
async def create_note(
        note_payload: NoteCreate,
        current: CurrentUser = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    note = Note(
        user_id=current.user.id,
        title=note_payload.title,
        content=note_payload.content,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
