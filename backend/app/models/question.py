# backend/app/models/question.py

from sqlalchemy import (
    BIGINT,
    SMALLINT,
    String,
    Text,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Question(Base):
    __tablename__ = "questions"

    # =========================
    # Columns
    # =========================

    question_id: Mapped[int] = mapped_column(
        SMALLINT,
        primary_key=True,
    )

    question_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    question_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        SMALLINT,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        server_default="true",
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    options = relationship(
        "QuestionOption",
        back_populates="question",
        cascade="all, delete-orphan",
    )

    answers = relationship(
        "Answer",
        back_populates="question",
    )

    question_set_items = relationship(
        "QuestionSetItem",
        back_populates="question",
        cascade="all, delete-orphan",
    )


class QuestionOption(Base):
    __tablename__ = "question_options"

    # =========================
    # Columns
    # =========================

    option_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    question_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey("questions.question_id"),
        nullable=False,
        index=True,
    )

    option_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    option_value: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    display_order: Mapped[int] = mapped_column(
        SMALLINT,
        nullable=False,
    )

    is_other: Mapped[bool] = mapped_column(
        Boolean,
        server_default="false",
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    question = relationship(
        "Question",
        back_populates="options",
    )

    answers = relationship(
        "Answer",
        back_populates="option",
    )


class QuestionSet(Base):
    __tablename__ = "question_sets"

    # =========================
    # Columns
    # =========================

    set_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    set_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    target_stage: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        server_default="true",
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    question_set_items = relationship(
        "QuestionSetItem",
        back_populates="question_set",
        cascade="all, delete-orphan",
    )


class QuestionSetItem(Base):
    __tablename__ = "question_set_items"

    # =========================
    # Composite Primary Key
    # =========================

    set_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("question_sets.set_id"),
        primary_key=True,
    )

    question_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey("questions.question_id"),
        primary_key=True,
    )

    display_order: Mapped[int] = mapped_column(
        SMALLINT,
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    question_set = relationship(
        "QuestionSet",
        back_populates="question_set_items",
    )

    question = relationship(
        "Question",
        back_populates="question_set_items",
    )