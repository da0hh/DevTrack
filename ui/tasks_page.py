from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QLineEdit, QTextEdit, QComboBox,
    QFormLayout, QMessageBox, QDateEdit
)
from PyQt6.QtCore import QDate

from services.task_service import (
    get_all_tasks, create_task, update_task,
    delete_task, search_tasks
)
from services.project_service import get_all_projects


class TaskDialog(QDialog):
    def __init__(self, task=None):
        super().__init__()

        self.setWindowTitle("Задача")
        self.setMinimumWidth(400)

        layout = QFormLayout(self)

        self.title = QLineEdit()
        self.description = QTextEdit()
        self.description.setMaximumHeight(90)

        self.project = QComboBox()
        self.projects = get_all_projects()

        for project in self.projects:
            self.project.addItem(project.name, project.id)

        self.priority = QComboBox()
        self.priority.addItems(["Низкий", "Средний", "Высокий"])

        self.status = QComboBox()
        self.status.addItems(["Не начата", "В процессе", "Выполнена"])

        self.deadline = QDateEdit()
        self.deadline.setCalendarPopup(True)
        self.deadline.setDisplayFormat("dd.MM.yyyy")
        self.deadline.setSpecialValueText("Без срока")
        self.deadline.setMinimumDate(QDate(2000, 1, 1))
        self.deadline.setDate(QDate.currentDate())
        self.deadline.setMinimumDate(QDate(2000, 1, 1))

        layout.addRow("Название:", self.title)
        layout.addRow("Описание:", self.description)
        layout.addRow("Проект:", self.project)
        layout.addRow("Приоритет:", self.priority)
        layout.addRow("Статус:", self.status)
        layout.addRow("Срок:", self.deadline)

        buttons = QHBoxLayout()
        save = QPushButton("Сохранить")
        cancel = QPushButton("Отмена")

        save.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)

        buttons.addWidget(save)
        buttons.addWidget(cancel)
        layout.addRow(buttons)

        if task:
            self.title.setText(task.title)
            self.description.setPlainText(task.description or "")
            self.priority.setCurrentText(task.priority)
            self.status.setCurrentText(task.status)

            index = self.project.findData(task.project_id)
            if index >= 0:
                self.project.setCurrentIndex(index)

            if task.deadline:
                self.deadline.setDate(
                    QDate(
                        task.deadline.year,
                        task.deadline.month,
                        task.deadline.day
                    )
                )

    def get_data(self):
        deadline = self.deadline.date().toPyDate()

        return (
            self.project.currentData(),
            self.title.text().strip(),
            self.description.toPlainText(),
            self.priority.currentText(),
            self.status.currentText(),
            deadline
        )


class TasksPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        header = QHBoxLayout()

        title = QLabel("Задачи")
        title.setObjectName("SectionTitle")

        add = QPushButton("+ Добавить задачу")
        add.clicked.connect(self.add_task)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(add)

        layout.addLayout(header)

        filters = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск по названию...")
        self.search.textChanged.connect(self.refresh)

        self.status_filter = QComboBox()
        self.status_filter.addItems([
            "Все статусы", "Не начата", "В процессе", "Выполнена"
        ])
        self.status_filter.currentTextChanged.connect(self.refresh)

        self.priority_filter = QComboBox()
        self.priority_filter.addItems([
            "Все приоритеты", "Низкий", "Средний", "Высокий"
        ])
        self.priority_filter.currentTextChanged.connect(self.refresh)

        filters.addWidget(self.search)
        filters.addWidget(self.status_filter)
        filters.addWidget(self.priority_filter)

        layout.addLayout(filters)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Название", "Проект", "Приоритет",
            "Статус", "Срок", "Описание"
        ])
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table)

        buttons = QHBoxLayout()

        edit = QPushButton("Редактировать")
        delete = QPushButton("Удалить")
        refresh = QPushButton("Обновить")

        edit.clicked.connect(self.edit_task)
        delete.clicked.connect(self.remove_task)
        refresh.clicked.connect(self.refresh)

        buttons.addWidget(edit)
        buttons.addWidget(delete)
        buttons.addStretch()
        buttons.addWidget(refresh)

        layout.addLayout(buttons)

        self.refresh()

    def refresh(self, *args):
        query = self.search.text().strip()
        status = self.status_filter.currentText()
        priority = self.priority_filter.currentText()

        tasks = search_tasks(query) if query else get_all_tasks()

        if status != "Все статусы":
            tasks = [t for t in tasks if t.status == status]

        if priority != "Все приоритеты":
            tasks = [t for t in tasks if t.priority == priority]

        self.table.setRowCount(len(tasks))

        projects = {p.id: p.name for p in get_all_projects()}

        for row, task in enumerate(tasks):
            values = [
                task.id,
                task.title,
                projects.get(task.project_id, "—"),
                task.priority,
                task.status,
                task.deadline.strftime("%d.%m.%Y") if task.deadline else "—",
                task.description
            ]

            for col, value in enumerate(values):
                self.table.setItem(
                    row, col, QTableWidgetItem(str(value or ""))
                )

    def selected_id(self):
        row = self.table.currentRow()

        if row < 0:
            return None

        return int(self.table.item(row, 0).text())

    def add_task(self):
        if not get_all_projects():
            QMessageBox.warning(
                self, "Ошибка", "Сначала создайте проект"
            )
            return

        dialog = TaskDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            project_id, title, description, priority, status, deadline = dialog.get_data()

            if not title:
                QMessageBox.warning(self, "Ошибка", "Введите название")
                return

            task_id = create_task(
                project_id, title, description, priority, deadline
            )

            update_task(
                task_id, project_id, title, description,
                priority, status, deadline
            )

            self.refresh()

    def edit_task(self):
        task_id = self.selected_id()

        if task_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу")
            return

        task = next(
            (t for t in get_all_tasks() if t.id == task_id),
            None
        )

        if task is None:
            return

        dialog = TaskDialog(task)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            project_id, title, description, priority, status, deadline = dialog.get_data()

            if not title:
                QMessageBox.warning(self, "Ошибка", "Введите название")
                return

            update_task(
                task_id, project_id, title, description,
                priority, status, deadline
            )

            self.refresh()

    def remove_task(self):
        task_id = self.selected_id()

        if task_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу")
            return

        answer = QMessageBox.question(
            self, "Удаление", "Удалить выбранную задачу?"
        )

        if answer == QMessageBox.StandardButton.Yes:
            delete_task(task_id)
            self.refresh()
