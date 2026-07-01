# backend/app/models/system.py

from sqlalchemy import (
    BIGINT,
    String,
    Text,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    func,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# ==========================================================
# Archive Event
# ==========================================================

class ArchiveEvent(Base):
    __tablename__ = "archive_events"

    event_id: Mapped[int] = mapped_column(
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

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    reference_id: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="archive_events",
    )


# ==========================================================
# Notification
# ==========================================================

class Notification(Base):
    __tablename__ = "notifications"

    notification_id: Mapped[int] = mapped_column(
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

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        server_default="false",
        nullable=False,
    )

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="notifications",
    )


# ==========================================================
# Prompt Version
# ==========================================================

class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    prompt_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    engine_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    prompt_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )


# ==========================================================
# RAG Source
# ==========================================================

class RagSource(Base):
    __tablename__ = "rag_sources"

    source_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    source_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    author: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )