from app.db.models.note import Note


def test_me_returns_user_info(client, db_session, mock_user):
    response = client.get("/me/")
    data = response.json()

    assert response.status_code == 200
    assert data["sub"] == mock_user.auth0_sub
    assert data["email"] == mock_user.email
    assert data["name"] == mock_user.name

    # Metadata viene de metadata_json + count_notes
    assert "metadata" in data
    assert "count_notes" in data["metadata"]

    note = Note(
        user_id=mock_user.id,
        title="Nota test",
        content="Contenido"
    )
    db_session.add(note)
    db_session.commit()

    response = client.get("/me/")
    data = response.json()

    assert response.status_code == 200
    assert data["metadata"]["count_notes"] == 1
