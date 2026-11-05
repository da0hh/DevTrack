from datetime import datetime, date

from sqlalchemy import (
    String,
    Text,
    Integer,
    Date,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(30), default="Активен")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    notes = relationship(
        "Note",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    time_sessions = relationship(
        "TimeSession",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    priority: Mapped[str] = mapped_column(String(20), default="Средний")
    status: Mapped[str] = mapped_column(String(30), default="Не начата")
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)

    project = relationship("Project", back_populates="tasks")


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id"),
        nullable=True
    )

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    project = relationship("Project", back_populates="notes")


class TimeSession(Base):
    __tablename__ = "time_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )
    task_id: Mapped[int | None] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=True
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
    duration: Mapped[int] = mapped_column(Integer, default=0)

    project = relationship("Project", back_populates="time_sessions")
    task = relationship("Task")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
