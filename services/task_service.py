from database.database import SessionLocal
from database.models import Task


def get_all_tasks():
    with SessionLocal() as session:
        return session.query(Task).order_by(Task.id.desc()).all()


def get_project_tasks(project_id):
    with SessionLocal() as session:
        return session.query(Task).filter(
            Task.project_id == project_id
        ).order_by(Task.id.desc()).all()


def create_task(project_id, title, description="", priority="Средний",
                deadline=None):
    with SessionLocal() as session:
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            priority=priority,
            deadline=deadline
        )
        session.add(task)
        session.commit()
        return task.id


def update_task(task_id, project_id, title, description,
                priority, status, deadline):
    with SessionLocal() as session:
        task = session.get(Task, task_id)

        if task is None:
            return False

        task.project_id = project_id
        task.title = title
        task.description = description
        task.priority = priority
        task.status = status
        task.deadline = deadline

        session.commit()
        return True

def delete_task(task_id):
    with SessionLocal() as session:
        task = session.get(Task, task_id)

        if task is None:
            return False

        session.delete(task)
        session.commit()
        return True


def search_tasks(query):
    with SessionLocal() as session:
        return session.query(Task).filter(
            Task.title.ilike(f"%{query}%")
        ).all()


def filter_tasks(status=None, priority=None):
    with SessionLocal() as session:
        query = session.query(Task)

        if status:
            query = query.filter(Task.status == status)

        if priority:
            query = query.filter(Task.priority == priority)

        return query.order_by(Task.id.desc()).all()
