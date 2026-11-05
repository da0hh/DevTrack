from datetime import datetime

from database.database import SessionLocal
from database.models import TimeSession


def start_session(project_id, task_id=None):
    with SessionLocal() as session:
        work_session = TimeSession(
            project_id=project_id,
            task_id=task_id,
            start_time=datetime.now(),
            end_time=None,
            duration=0
        )

        session.add(work_session)
        session.commit()
        return work_session.id


def stop_session(session_id):
    with SessionLocal() as session:
        work_session = session.get(TimeSession, session_id)

        if work_session is None or work_session.end_time is not None:
            return False

        work_session.end_time = datetime.now()
        work_session.duration = int(
            (work_session.end_time - work_session.start_time).total_seconds()
        )

        session.commit()
        return work_session.duration


def get_all_sessions():
    with SessionLocal() as session:
        return session.query(TimeSession).order_by(
            TimeSession.id.desc()
        ).all()


def get_project_time(project_id):
    with SessionLocal() as session:
        sessions = session.query(TimeSession).filter(
            TimeSession.project_id == project_id
        ).all()

        return sum(item.duration for item in sessions)
