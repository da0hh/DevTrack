from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QLineEdit, QTextEdit,
    QComboBox, QMessageBox, QFileDialog
)

from services.note_service import (
    get_all_notes, create_note, update_note, delete_note
)
from services.project_service import get_all_projects


class NotesPage(QWidget):
    def __init__(self):
        super().__init__()

        self.current_note_id = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)

        title = QLabel("Технические заметки")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)

        content = QHBoxLayout()

        self.notes_list = QListWidget()
        self.notes_list.setMinimumWidth(220)
        self.notes_list.currentRowChanged.connect(self.select_note)
        content.addWidget(self.notes_list)

        editor = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название заметки")

        self.project = QComboBox()
        self.project.addItem("Без проекта", None)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Содержимое заметки...")

        editor.addWidget(self.title_input)
        editor.addWidget(self.project)
        editor.addWidget(self.content_input)

        content.addLayout(editor)
        layout.addLayout(content)

        buttons = QHBoxLayout()

        save = QPushButton("Сохранить")
        new = QPushButton("Новая заметка")
        delete = QPushButton("Удалить")
        export = QPushButton("Экспорт TXT")

        save.clicked.connect(self.save_note)
        new.clicked.connect(self.new_note)
        delete.clicked.connect(self.remove_note)
        export.clicked.connect(self.export_note)

        for button in [new, save, delete, export]:
            buttons.addWidget(button)

        layout.addLayout(buttons)

        self.refresh()

    def refresh(self):
        current_id = self.current_note_id

        self.notes_list.blockSignals(True)
        self.notes_list.clear()

        notes = get_all_notes()

        for note in notes:
            self.notes_list.addItem(note.title)

        self.notes_list.blockSignals(False)

        self.notes = notes

        projects = get_all_projects()
        self.project.clear()
        self.project.addItem("Без проекта", None)

        for project in projects:
            self.project.addItem(project.name, project.id)

        if current_id is not None:
            for i, note in enumerate(notes):
                if note.id == current_id:
                    self.notes_list.setCurrentRow(i)
                    return

        self.notes_list.setCurrentRow(-1)

    def select_note(self, row):
        if row < 0 or row >= len(self.notes):
            return

        note = self.notes[row]
        self.current_note_id = note.id

        self.title_input.setText(note.title)
        self.content_input.setPlainText(note.content)

        index = self.project.findData(note.project_id)
        self.project.setCurrentIndex(max(index, 0))

    def new_note(self):
        self.current_note_id = None
        self.notes_list.setCurrentRow(-1)
        self.title_input.clear()
        self.content_input.clear()
        self.project.setCurrentIndex(0)

    def save_note(self):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText()
        project_id = self.project.currentData()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название заметки")
            return

        if self.current_note_id is None:
            self.current_note_id = create_note(
                title, content, project_id
            )
        else:
            update_note(
                self.current_note_id, title, content, project_id
            )

        self.refresh()

        QMessageBox.information(
            self, "Готово", "Заметка сохранена"
        )

    def remove_note(self):
        if self.current_note_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите заметку")
            return

        answer = QMessageBox.question(
            self, "Удаление", "Удалить заметку?"
        )

        if answer == QMessageBox.StandardButton.Yes:
            delete_note(self.current_note_id)
            self.new_note()
            self.refresh()

    def export_note(self):
        title = self.title_input.text().strip()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Нет заметки для экспорта")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить заметку", f"{title}.txt", "Text files (*.txt)"
        )

        if path:
            Path(path).write_text(
                self.content_input.toPlainText(),
                encoding="utf-8"
            )
