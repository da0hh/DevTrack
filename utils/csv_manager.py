import csv

from services.project_service import get_all_projects
from services.task_service import get_all_tasks


def export_projects(path):
    projects = get_all_projects()

    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")

        writer.writerow([
            "ID", "Название", "Описание", "Статус", "Дата создания"
        ])

        for project in projects:
            writer.writerow([
                project.id,
                project.name,
                project.description,
                project.status,
                project.created_at
            ])


def export_tasks(path):
    tasks = get_all_tasks()

    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")

        writer.writerow([
            "ID", "Project ID", "Название", "Описание",
            "Приоритет", "Статус", "Срок"
        ])

        for task in tasks:
            writer.writerow([
                task.id,
                task.project_id,
                task.title,
                task.description,
                task.priority,
                task.status,
                task.deadline
            ])


def import_projects(path):
    from services.project_service import create_project

    count = 0

    with open(path, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            name = row.get("Название", "").strip()

            if name:
                create_project(
                    name,
                    row.get("Описание", "")
                )
                count += 1

    return count


def import_tasks(path):
    from services.task_service import create_task

    count = 0

    with open(path, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            title = row.get("Название", "").strip()

            if not title:
                continue

            try:
                project_id = int(row["Project ID"])
            except (ValueError, KeyError):
                continue

            from services.project_service import get_project

            if get_project(project_id) is None:
                continue

            from datetime import date

            deadline_text = row.get("Срок", "").strip()
            deadline = None

            if deadline_text:
                try:
                    deadline = date.fromisoformat(deadline_text)
                except ValueError:
                    pass

            task_id = create_task(
                project_id,
                title,
                row.get("Описание", ""),
                row.get("Приоритет", "Средний"),
                deadline
            )

            from services.task_service import update_task

            update_task(
                task_id,
                project_id,
                title,
                row.get("Описание", ""),
                row.get("Приоритет", "Средний"),
                row.get("Статус", "Не начата"),
                deadline
            )

            count += 1

    return count
