from app.db.models.note import Note


def test_create_note(client, db_session, mock_user):
    payload = {
        "title": "Seguimiento productor",
        "content": "Esto es una nota"
    }

    response = client.post("/notes/", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert data["id"] > 0


def test_list_notes(client, db_session, mock_user):
    # Crear notas manualmente en DB
    note = Note(
        user_id=mock_user.id,
        title="Nota test",
        content="Contenido"
    )
    db_session.add(note)
    db_session.commit()

    response = client.get("/notes/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 1

    first = data[0]
    assert "title" in first
    assert "content" in first
    assert "created_at" in first
