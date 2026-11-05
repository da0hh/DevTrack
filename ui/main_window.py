from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt

from ui.dashboard import DashboardPage
from ui.projects_page import ProjectsPage
from ui.tasks_page import TasksPage
from ui.notes_page import NotesPage
from ui.timer_page import TimerPage
from ui.statistics_page import StatisticsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DevTrack")
        self.resize(1200, 750)
        self.setMinimumSize(950, 600)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #111827;
                color: #F9FAFB;
                font-family: Segoe UI;
                font-size: 13px;
            }

            QFrame#Sidebar {
                background-color: #1F2937;
                border: none;
            }

            QPushButton {
                background-color: #374151;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 11px;
                text-align: left;
            }

            QPushButton:hover {
                background-color: #4B5563;
            }

            QPushButton:checked {
                background-color: #2563EB;
            }

            QLabel#Title {
                font-size: 23px;
                font-weight: bold;
            }

            QLabel#SectionTitle {
                font-size: 20px;
                font-weight: bold;
            }

            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                background-color: #374151;
                border: 1px solid #4B5563;
                border-radius: 5px;
                padding: 7px;
                color: white;
            }

            QTableWidget {
                background-color: #1F2937;
                alternate-background-color: #263244;
                gridline-color: #374151;
                border: none;
            }

            QHeaderView::section {
                background-color: #374151;
                padding: 8px;
                border: none;
            }

            QTableWidget::item {
                padding: 6px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)

        logo = QLabel("DevTrack")
        logo.setObjectName("Title")
        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(25)

        self.stack = QStackedWidget()

        self.pages = [
            DashboardPage(),
            ProjectsPage(),
            TasksPage(),
            NotesPage(),
            TimerPage(),
            StatisticsPage()
        ]

        for page in self.pages:
            self.stack.addWidget(page)

        tabs = [
            'Главная',
            'Проекты',
            'Задачи',
            'Заметки',
            'Учёт времени',
            'Статистика'
        ]

        self.buttons = []

        for index, tab in enumerate(tabs):
            button = QPushButton(tab)
            button.setCheckable(True)
            button.clicked.connect(
                lambda checked, i=index: self.change_page(i)
            )

            sidebar_layout.addWidget(button)
            self.buttons.append(button)

        sidebar_layout.addStretch()
        version = QLabel("DevTrack v1.0")
        version.setStyleSheet("color: #9CA3AF;")
        sidebar_layout.addWidget(version)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)


        self.change_page(0)

    def change_page(self, index):
        self.stack.setCurrentIndex(index)

        for i, button in enumerate(self.buttons):
            button.setChecked(i == index)

        page = self.pages[index]
        if hasattr(page, "refresh"):
            page.refresh()