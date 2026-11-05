from database.database import SessionLocal
from database.models import Project


def get_all_projects():
    with SessionLocal() as session:
        return session.query(Project).order_by(Project.id.desc()).all()


def get_project(project_id):
    with SessionLocal() as session:
        return session.get(Project, project_id)


def create_project(name, description=""):
    with SessionLocal() as session:
        project = Project(name=name, description=description)
        session.add(project)
        session.commit()
        session.refresh(project)
        return project.id


def update_project(project_id, name, description, status):
    with SessionLocal() as session:
        project = session.get(Project, project_id)

        if project is None:
            return False

        project.name = name
        project.description = description
        project.status = status

        session.commit()
        return True


def delete_project(project_id):
    with SessionLocal() as session:
        project = session.get(Project, project_id)

        if project is None:
            return False

        session.delete(project)
        session.commit()
        return True
