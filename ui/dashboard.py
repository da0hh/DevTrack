from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)

from services.statistics_service import get_statistics


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 25, 30, 25)
        self.layout.setSpacing(20)

        title = QLabel("Главная")
        title.setObjectName("SectionTitle")
        self.layout.addWidget(title)

        subtitle = QLabel("Обзор твоей разработки")
        subtitle.setStyleSheet("color: #9CA3AF;")
        self.layout.addWidget(subtitle)

        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(15)
        self.layout.addLayout(self.cards_layout)

        self.info_label = QLabel()
        self.info_label.setStyleSheet(
            "font-size: 15px; color: #D1D5DB;"
        )
        self.layout.addWidget(self.info_label)

        self.layout.addStretch()
        self.refresh()

    def create_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout(card)

        name = QLabel(title)
        name.setStyleSheet("color: #9CA3AF;")

        number = QLabel(str(value))
        number.setStyleSheet(
            "font-size: 27px; font-weight: bold; color: #60A5FA;"
        )

        layout.addWidget(name)
        layout.addWidget(number)

        return card

    def refresh(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        stats = get_statistics()

        cards = [
            ("Проекты", stats["projects"]),
            ("Активные проекты", stats["active_projects"]),
            ("Всего задач", stats["tasks"]),
            ("Выполнено задач", stats["completed_tasks"]),
            ("Прогресс", f'{stats["progress"]}%')
        ]

        for title, value in cards:
            self.cards_layout.addWidget(
                self.create_card(title, value)
            )

        hours = stats["total_hours"]

        self.info_label.setText(
            f"Всего затрачено времени: {hours} ч.\n"
            f"Общий прогресс выполнения задач: {stats['progress']}%"
        )
