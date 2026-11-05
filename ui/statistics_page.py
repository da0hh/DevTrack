
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QGridLayout
)

from services.statistics_service import get_statistics


class StatisticsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 25, 30, 25)
        self.main_layout.setSpacing(20)

        title = QLabel("Статистика")
        title.setObjectName("SectionTitle")
        self.main_layout.addWidget(title)

        self.cards = QGridLayout()
        self.cards.setSpacing(15)
        self.main_layout.addLayout(self.cards)

        self.main_layout.addStretch()
        self.refresh()

    def refresh(self):
        while self.cards.count():
            item = self.cards.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        stats = get_statistics()

        values = [
            ("Всего проектов", stats["projects"]),
            ("Активных проектов", stats["active_projects"]),
            ("Всего задач", stats["tasks"]),
            ("Завершённых задач", stats["completed_tasks"]),
            ("Общий прогресс", f'{stats["progress"]}%'),
            ("Затраченное время", f'{stats["total_hours"]} часов')
        ]

        for index, (name, value) in enumerate(values):
            card = QFrame()
            card.setMinimumHeight(100)
            card.setStyleSheet("""
                QFrame {
                    background-color: #1F2937;
                    border-radius: 8px;
                }
            """)

            row = QVBoxLayout(card)
            row.setContentsMargins(15, 12, 15, 12)

            label = QLabel(name)
            label.setStyleSheet("color: #9CA3AF;")

            number = QLabel(str(value))
            number.setStyleSheet("""
                font-size: 22px;
                font-weight: bold;
                color: #60A5FA;
            """)

            row.addWidget(label)
            row.addWidget(number)

            self.cards.addWidget(card, index // 2, index % 2)
