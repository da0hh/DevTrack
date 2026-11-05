from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QMessageBox
)
from PyQt6.QtCore import QTimer

from services.project_service import get_all_projects
from services.task_service import get_project_tasks
from services.timer_service import start_session, stop_session


class TimerPage(QWidget):
    def __init__(self):
        super().__init__()

        self.session_id = None
        self.elapsed = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)

        title = QLabel("Учёт рабочего времени")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)

        self.project = QComboBox()
        self.project.currentIndexChanged.connect(self.load_tasks)

        self.task = QComboBox()
        self.task.addItem("Без задачи", None)

        self.clock = QLabel("00:00:00")
        self.clock.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock.setStyleSheet("""
            font-size: 55px;
            font-weight: bold;
            color: #60A5FA;
            padding: 30px;
        """)

        self.status = QLabel("Таймер остановлен")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttons = QHBoxLayout()

        self.start_button = QPushButton("Начать")
        self.stop_button = QPushButton("Остановить")

        self.start_button.clicked.connect(self.start_timer)
        self.stop_button.clicked.connect(self.stop_timer)

        buttons.addWidget(self.start_button)
        buttons.addWidget(self.stop_button)

        layout.addWidget(QLabel("Проект:"))
        layout.addWidget(self.project)
        layout.addWidget(QLabel("Задача:"))
        layout.addWidget(self.task)
        layout.addStretch()
        layout.addWidget(self.clock)
        layout.addWidget(self.status)
        layout.addLayout(buttons)
        layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

        self.refresh()

    def refresh(self):
        if self.session_id is not None:
            return

        self.project.clear()

        for project in get_all_projects():
            self.project.addItem(project.name, project.id)

        self.load_tasks()

    def load_tasks(self, *args):
        self.task.clear()
        self.task.addItem("Без задачи", None)

        project_id = self.project.currentData()

        if project_id is None:
            return

        for task in get_project_tasks(project_id):
            self.task.addItem(task.title, task.id)

    def start_timer(self):
        if self.session_id is not None:
            return

        project_id = self.project.currentData()

        if project_id is None:
            QMessageBox.warning(
                self, "Ошибка", "Сначала создайте и выберите проект"
            )
            return

        self.elapsed = 0
        self.session_id = start_session(
            project_id, self.task.currentData()
        )

        self.timer.start(1000)
        self.status.setText("Рабочая сессия активна")
        self.start_button.setEnabled(False)
        self.project.setEnabled(False)
        self.task.setEnabled(False)

    def tick(self):
        self.elapsed += 1

        hours = self.elapsed // 3600
        minutes = (self.elapsed % 3600) // 60
        seconds = self.elapsed % 60

        self.clock.setText(
            f"{hours:02}:{minutes:02}:{seconds:02}"
        )

    def stop_timer(self):
        if self.session_id is None:
            return

        stop_session(self.session_id)

        self.timer.stop()
        self.session_id = None

        self.status.setText("Рабочая сессия завершена")
        self.start_button.setEnabled(True)
        self.project.setEnabled(True)
        self.task.setEnabled(True)
