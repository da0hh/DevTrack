from PyQt6.QtWidgets import QFileDialog
from utils.csv_manager import export_projects, import_projects

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QLineEdit, QTextEdit, QComboBox,
    QFormLayout, QMessageBox
)

from services.project_service import (
    get_all_projects,
    create_project,
    update_project,
    delete_project
)


class ProjectDialog(QDialog):
    def __init__(self, project=None):
        super().__init__()

        self.setWindowTitle("Проект")
        self.setMinimumWidth(400)

        layout = QFormLayout(self)

        self.name = QLineEdit()
        self.description = QTextEdit()
        self.description.setMaximumHeight(100)

        self.status = QComboBox()
        self.status.addItems(["Активен", "Завершён", "Приостановлен"])

        layout.addRow("Название:", self.name)
        layout.addRow("Описание:", self.description)
        layout.addRow("Статус:", self.status)

        buttons = QHBoxLayout()
        save = QPushButton("Сохранить")
        cancel = QPushButton("Отмена")

        save.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)

        buttons.addWidget(save)
        buttons.addWidget(cancel)
        layout.addRow(buttons)

        if project:
            self.name.setText(project.name)
            self.description.setPlainText(project.description or "")
            self.status.setCurrentText(project.status)

    def get_data(self):
        return (
            self.name.text().strip(),
            self.description.toPlainText(),
            self.status.currentText()
        )


class ProjectsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        header = QHBoxLayout()

        title = QLabel("Мои проекты")
        title.setObjectName("SectionTitle")

        add_button = QPushButton("+ Добавить проект")
        add_button.clicked.connect(self.add_project)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(add_button)

        layout.addLayout(header)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Название", "Описание", "Статус", "Дата создания"
        ])
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table)

        buttons = QHBoxLayout()

        edit = QPushButton("Редактировать")
        delete = QPushButton("Удалить")
        refresh = QPushButton("Обновить")

        edit.clicked.connect(self.edit_project)
        delete.clicked.connect(self.remove_project)
        refresh.clicked.connect(self.refresh)

        buttons.addWidget(edit)
        buttons.addWidget(delete)
        buttons.addStretch()
        buttons.addWidget(refresh)

        export = QPushButton("Экспорт CSV")
        import_button = QPushButton("Импорт CSV")

        export.clicked.connect(self.export_csv)
        import_button.clicked.connect(self.import_csv)

        buttons.addWidget(export)
        buttons.addWidget(import_button)

        layout.addLayout(buttons)

        self.refresh()

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт проектов", "projects.csv", "CSV (*.csv)"
        )

        if path:
            export_projects(path)
            QMessageBox.information(self, "Готово", "Проекты экспортированы")

    def import_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Импорт проектов", "", "CSV (*.csv)"
        )

        if path:
            try:
                count = import_projects(path)
                self.refresh()
                QMessageBox.information(
                    self, "Готово", f"Импортировано проектов: {count}"
                )
            except Exception as error:
                QMessageBox.critical(self, "Ошибка", str(error))

    def refresh(self):
        projects = get_all_projects()

        self.table.setRowCount(len(projects))

        for row, project in enumerate(projects):
            values = [
                project.id,
                project.name,
                project.description,
                project.status,
                project.created_at.strftime("%d.%m.%Y")
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

    def add_project(self):
        dialog = ProjectDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, description, status = dialog.get_data()

            if not name:
                QMessageBox.warning(self, "Ошибка", "Введите название проекта")
                return

            project_id = create_project(name, description)

            if status != "Активен":
                update_project(project_id, name, description, status)

            self.refresh()

    def edit_project(self):
        project_id = self.selected_id()

        if project_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите проект")
            return

        project = next(
            (p for p in get_all_projects() if p.id == project_id),
            None
        )

        if project is None:
            return

        dialog = ProjectDialog(project)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, description, status = dialog.get_data()

            if not name:
                QMessageBox.warning(self, "Ошибка", "Введите название")
                return

            update_project(project_id, name, description, status)
            self.refresh()

    def remove_project(self):
        project_id = self.selected_id()

        if project_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите проект")
            return

        answer = QMessageBox.question(
            self,
            "Удаление",
            "Удалить проект и связанные с ним задачи, заметки и сессии?"
        )

        if answer == QMessageBox.StandardButton.Yes:
            try:
                delete_project(project_id)
                self.refresh()
            except Exception as error:
                QMessageBox.critical(self, "Ошибка", str(error))
