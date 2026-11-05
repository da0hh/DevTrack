from sqlalchemy import func

from database.database import SessionLocal
from database.models import Project, Task, TimeSession


def get_statistics():
    with SessionLocal() as session:
        projects_count = session.query(Project).count()
        tasks_count = session.query(Task).count()

        completed_tasks = session.query(Task).filter(
            Task.status == "Выполнена"
        ).count()

        active_projects = session.query(Project).filter(
            Project.status == "Активен"
        ).count()

        total_seconds = session.query(
            func.coalesce(func.sum(TimeSession.duration), 0)
        ).scalar()

        progress = (
            round(completed_tasks / tasks_count * 100)
            if tasks_count else 0
        )

        return {
            "projects": projects_count,
            "active_projects": active_projects,
            "tasks": tasks_count,
            "completed_tasks": completed_tasks,
            "progress": progress,
            "total_seconds": total_seconds,
            "total_hours": round(total_seconds / 3600, 2)
        }
