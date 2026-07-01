# backend/app/models/identity.py

from sqlalchemy import (
    BIGINT,
    SMALLINT,
    INTEGER,
    DECIMAL,
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
# Identity
# ==========================================================

class Identity(Base):
    __tablename__ = "identities"

    identity_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("users.user_id"),
        nullable=False,
    )

    identity_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    confidence: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        server_default="0",
        nullable=False,
    )

    version: Mapped[int] = mapped_column(
        INTEGER,
        server_default="1",
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

    # Relationships

    user = relationship(
        "User",
        back_populates="identities",
    )

    keyword_maps = relationship(
        "IdentityKeywordMap",
        back_populates="identity",
        cascade="all, delete-orphan",
    )

    strengths = relationship(
        "IdentityStrength",
        back_populates="identity",
        cascade="all, delete-orphan",
    )

    growth_points = relationship(
        "IdentityGrowthPoint",
        back_populates="identity",
        cascade="all, delete-orphan",
    )

    operating_systems = relationship(
        "OperatingSystem",
        back_populates="identity",
    )


# ==========================================================
# Identity Keyword
# ==========================================================

class IdentityKeyword(Base):
    __tablename__ = "identity_keywords"

    keyword_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    keyword_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    category: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # Relationships

    keyword_maps = relationship(
        "IdentityKeywordMap",
        back_populates="keyword",
    )


# ==========================================================
# Identity Keyword Map
# ==========================================================

class IdentityKeywordMap(Base):
    __tablename__ = "identity_keyword_maps"

    identity_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("identities.identity_id"),
        primary_key=True,
    )

    keyword_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("identity_keywords.keyword_id"),
        primary_key=True,
    )

    weight: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        server_default="1",
        nullable=False,
    )

    # Relationships

    identity = relationship(
        "Identity",
        back_populates="keyword_maps",
    )

    keyword = relationship(
        "IdentityKeyword",
        back_populates="keyword_maps",
    )


# ==========================================================
# Identity Strength
# ==========================================================

class IdentityStrength(Base):
    __tablename__ = "identity_strengths"

    strength_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    identity_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("identities.identity_id"),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        SMALLINT,
        server_default="1",
        nullable=False,
    )

    # Relationships

    identity = relationship(
        "Identity",
        back_populates="strengths",
    )


# ==========================================================
# Identity Growth Point
# ==========================================================

class IdentityGrowthPoint(Base):
    __tablename__ = "identity_growth_points"

    growth_point_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    identity_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("identities.identity_id"),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        SMALLINT,
        server_default="1",
        nullable=False,
    )

    # Relationships

    identity = relationship(
        "Identity",
        back_populates="growth_points",
    )