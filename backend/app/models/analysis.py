# backend/app/models/analysis.py

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


class PatternAnalysis(Base):
    __tablename__ = "pattern_analysis"

    # 상태값 제한
    __table_args__ = ()

    # =========================
    # Columns
    # =========================

    pattern_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    scan_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(
            "scans.scan_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    future_score: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    creativity_score: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    execution_score: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    uncertainty_score: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    perfectionism_score: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    resilience_score: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    model_version: Mapped[str] = mapped_column(
        String(50),
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
        back_populates="pattern_analysis",
    )

    insights = relationship(
        "Insight",
        back_populates="pattern_analysis",
        cascade="all, delete-orphan",
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="pattern_analysis",
        cascade="all, delete-orphan",
    )

    recommendation_generations = relationship(
        "RecommendationGeneration",
        back_populates="pattern_analysis",
        cascade="all, delete-orphan",
    )

    growth_analysis = relationship(
        "GrowthAnalysis",
        back_populates="pattern_analysis",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )


class Insight(Base):
    __tablename__ = "insights"

    # =========================
    # Columns
    # =========================

    insight_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    pattern_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("pattern_analysis.pattern_id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    priority: Mapped[int] = mapped_column(
        SMALLINT,
        server_default="1",
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

    pattern_analysis = relationship(
        "PatternAnalysis",
        back_populates="insights",
    )


class Recommendation(Base):
    __tablename__ = "recommendations"

    __table_args__ = (
        CheckConstraint(
            "status IN ('WAITING', 'DOING', 'DONE')",
            name="ck_recommendation_status",
        ),
    )

    # =========================
    # Columns
    # =========================

    recommendation_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    generation_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(
            "recommendation_generations.generation_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    pattern_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("pattern_analysis.pattern_id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    priority: Mapped[int] = mapped_column(
        SMALLINT,
        server_default="1",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        server_default="WAITING",
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

    pattern_analysis = relationship(
        "PatternAnalysis",
        back_populates="recommendations",
    )

    next_actions = relationship(
        "NextAction",
        back_populates="recommendation",
        cascade="all, delete-orphan",
    )

    generation = relationship(
        "RecommendationGeneration",
        back_populates="recommendations",
    )

class DataConfidence(Base):
    __tablename__ = "data_confidence"

    # =========================
    # Columns
    # =========================

    confidence_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("users.user_id"),
        nullable=False,
        unique=True,
    )

    scan_count: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
    )

    confidence_score: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    current_stage: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    user = relationship(
        "User",
        back_populates="data_confidence",
    )


class RecommendationGeneration(Base):
    __tablename__ = "recommendation_generations"

    generation_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    pattern_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(
            "pattern_analysis.pattern_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    confidence: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(30),
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

    pattern_analysis = relationship(
        "PatternAnalysis",
        back_populates="recommendation_generations",
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="generation",
        cascade="all, delete-orphan",
    )
