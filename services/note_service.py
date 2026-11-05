from database.database import SessionLocal
from database.models import Note


def get_all_notes():
    with SessionLocal() as session:
        return session.query(Note).order_by(Note.id.desc()).all()


def create_note(title, content, project_id=None):
    with SessionLocal() as session:
        note = Note(
            title=title,
            content=content,
            project_id=project_id
        )
        session.add(note)
        session.commit()
        return note.id


def update_note(note_id, title, content, project_id=None):
    with SessionLocal() as session:
        note = session.get(Note, note_id)

        if note is None:
            return False

        note.title = title
        note.content = content
        note.project_id = project_id

        session.commit()
        return True


def delete_note(note_id):
    with SessionLocal() as session:
        note = session.get(Note, note_id)

        if note is None:
            return False

        session.delete(note)
        session.commit()
        return True
