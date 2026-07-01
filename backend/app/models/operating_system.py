# backend/app/models/operating_system.py

from sqlalchemy import (
    BIGINT,
    SMALLINT,
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
# Operating System
# ==========================================================

class OperatingSystem(Base):
    __tablename__ = "operating_systems"

    os_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("users.user_id"),
        nullable=False,
    )

    identity_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("identities.identity_id"),
        nullable=False,
    )

    life_map_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("life_maps.life_map_id"),
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    generated_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        server_default="true",
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    user = relationship(
        "User",
        back_populates="operating_systems",
    )

    identity = relationship(
        "Identity",
        back_populates="operating_systems",
    )

    life_map = relationship(
        "LifeMap",
        back_populates="operating_systems",
    )

    core_values = relationship(
        "OSCoreValue",
        back_populates="operating_system",
        cascade="all, delete-orphan",
    )


# ==========================================================
# Core Value
# ==========================================================

class CoreValue(Base):
    __tablename__ = "core_values"

    value_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    value_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # =========================
    # Relationships
    # =========================

    operating_systems = relationship(
        "OSCoreValue",
        back_populates="core_value",
        cascade="all, delete-orphan",
    )


# ==========================================================
# OS Core Value (Mapping Table)
# ==========================================================

class OSCoreValue(Base):
    __tablename__ = "os_core_values"

    os_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("operating_systems.os_id"),
        primary_key=True,
    )

    value_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("core_values.value_id"),
        primary_key=True,
    )

    priority: Mapped[int] = mapped_column(
        SMALLINT,
        server_default="1",
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    operating_system = relationship(
        "OperatingSystem",
        back_populates="core_values",
    )

    core_value = relationship(
        "CoreValue",
        back_populates="operating_systems",
    )