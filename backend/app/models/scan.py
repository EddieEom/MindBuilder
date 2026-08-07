# backend/app/models/scan.py

from sqlalchemy import (
    BIGINT,
    SMALLINT,
    INTEGER,
    DECIMAL,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    CheckConstraint,
    func,
)
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Scan(Base):
    __tablename__ = "scans"

    __table_args__ = (
        CheckConstraint(
            "status IN ('IN_PROGRESS', 'COMPLETED', 'FAILED')",
            name="ck_scan_status",
        ),
    )

    # =========================
    # Columns
    # =========================

    scan_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("users.user_id"),
        nullable=False,
        index=True,
    )

    scan_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        server_default="IN_PROGRESS",
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    user = relationship(
        "User",
        back_populates="scans",
    )

    answers = relationship(
        "Answer",
        back_populates="scan",
        cascade="all, delete-orphan",
    )

    feature_values = relationship(
        "FeatureValue",
        back_populates="scan",
        cascade="all, delete-orphan",
    )

    pattern_analysis = relationship(
        "PatternAnalysis",
        back_populates="scan",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )


class Answer(Base):
    __tablename__ = "answers"

    # =========================
    # Columns
    # =========================

    answer_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    scan_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("scans.scan_id"),
        nullable=False,
        index=True,
    )

    question_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey("questions.question_id"),
        nullable=False,
    )

    option_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("question_options.option_id"),
        nullable=False,
    )

    point_value: Mapped[int] = mapped_column(
        INTEGER,
        server_default="0",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    scan = relationship(
        "Scan",
        back_populates="answers",
    )

    question = relationship(
        "Question",
        back_populates="answers",
    )

    option = relationship(
        "QuestionOption",
        back_populates="answers",
    )

    detail = relationship(
        "AnswerDetail",
        back_populates="answer",
        uselist=False,
        cascade="all, delete-orphan",
    )


class AnswerDetail(Base):
    __tablename__ = "answer_details"

    # =========================
    # Columns
    # =========================

    detail_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    answer_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("answers.answer_id"),
        nullable=False,
        unique=True,
    )

    detail_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    answer = relationship(
        "Answer",
        back_populates="detail",
    )


class FeatureValue(Base):
    __tablename__ = "feature_values"

    # =========================
    # Columns
    # =========================

    feature_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    scan_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("scans.scan_id"),
        nullable=False,
        index=True,
    )

    feature_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    feature_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    feature_value: Mapped[float] = mapped_column(
        DECIMAL(6, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    scan = relationship(
        "Scan",
        back_populates="feature_values",
    )
