# backend/app/models/growth.py

from sqlalchemy import (
    BIGINT,
    SMALLINT,
    DECIMAL,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    func,
    CheckConstraint
)
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# ==========================================================
# Growth Analysis
# ==========================================================

class GrowthAnalysis(Base):
    __tablename__ = "growth_analysis"

    growth_analysis_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    pattern_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("pattern_analysis.pattern_id"),
        nullable=False,
        unique=True,
    )

    analysis_version: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    llm_model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    # Relationships

    pattern_analysis = relationship(
        "PatternAnalysis",
        back_populates="growth_analysis",
    )

    growth_items = relationship(
        "GrowthItem",
        back_populates="growth_analysis",
        cascade="all, delete-orphan",
    )

    feedbacks = relationship(
        "Feedback",
        back_populates="growth_analysis",
        cascade="all, delete-orphan",
    )


# ==========================================================
# Growth Item Type
# ==========================================================

class GrowthItemType(Base):
    __tablename__ = "growth_item_types"

    type_id: Mapped[int] = mapped_column(
        SMALLINT,
        primary_key=True,
        autoincrement=True,
    )

    type_name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        SMALLINT,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Relationships

    growth_items = relationship(
        "GrowthItem",
        back_populates="growth_item_type",
    )


# ==========================================================
# Growth Item
# ==========================================================

class GrowthItem(Base):
    __tablename__ = "growth_items"

    growth_item_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    growth_analysis_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("growth_analysis.growth_analysis_id"),
        nullable=False,
    )

    type_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey("growth_item_types.type_id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
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

    # Relationships

    growth_analysis = relationship(
        "GrowthAnalysis",
        back_populates="growth_items",
    )

    growth_item_type = relationship(
        "GrowthItemType",
        back_populates="growth_items",
    )

    explanations = relationship(
        "AIExplanation",
        back_populates="growth_item",
        cascade="all, delete-orphan",
    )


# ==========================================================
# Explanation Type
# ==========================================================

class ExplanationType(Base):
    __tablename__ = "explanation_types"

    type_id: Mapped[int] = mapped_column(
        SMALLINT,
        primary_key=True,
        autoincrement=True,
    )

    type_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    type_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        SMALLINT,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Relationships

    explanations = relationship(
        "AIExplanation",
        back_populates="explanation_type",
    )


# ==========================================================
# AI Explanation
# ==========================================================

class AIExplanation(Base):
    __tablename__ = "ai_explanations"

    explanation_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    growth_item_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("growth_items.growth_item_id"),
        nullable=False,
    )

    type_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey("explanation_types.type_id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        server_default="0",
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        SMALLINT,
        server_default="1",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    # Relationships

    growth_item = relationship(
        "GrowthItem",
        back_populates="explanations",
    )

    explanation_type = relationship(
        "ExplanationType",
        back_populates="explanations",
    )


# ==========================================================
# Explanation Source
# ==========================================================

class ExplanationSource(Base):
    __tablename__ = "explanation_sources"

    source_id: Mapped[int] = mapped_column(
        SMALLINT,
        primary_key=True,
        autoincrement=True,
    )

    source_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    source_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


# ==========================================================
# Feedback
# ==========================================================

class Feedback(Base):
    __tablename__ = "feedbacks"

    __table_args__ = (
        CheckConstraint(
            "rating BETWEEN 1 AND 5",
            name="ck_feedback_rating",
        ),
    )

    feedback_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    growth_analysis_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("growth_analysis.growth_analysis_id"),
        nullable=False,
        unique=True,
    )

    rating: Mapped[int] = mapped_column(
        SMALLINT,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    # Relationships

    growth_analysis = relationship(
        "GrowthAnalysis",
        back_populates="feedbacks",
    )


# ==========================================================
# Next Action
# ==========================================================

class NextAction(Base):
    __tablename__ = "next_actions"

    __table_args__ = (
        CheckConstraint(
            "status IN ('WAITING', 'DOING', 'DONE')",
            name="ck_next_action_status",
        ),
    )

    action_id: Mapped[int] = mapped_column(
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

    recommendation_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("recommendations.recommendation_id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        server_default="WAITING",
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="next_actions",
    )

    recommendation = relationship(
        "Recommendation",
        back_populates="next_actions",
    )

