# backend/app/models/user.py
from sqlalchemy import Boolean, Integer, String, TIMESTAMP, ForeignKey, BIGINT, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import List
from datetime import datetime
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False)
    profile_image: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), server_default="ACTIVE", nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)

    # Relationships
    oauth_accounts: Mapped[List["OAuthAccount"]] = relationship("OAuthAccount",back_populates="user",cascade="all, delete-orphan",)
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(back_populates="user", cascade="all, delete-orphan",)

    # 추가
    scans = relationship(
        "Scan",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    data_confidence = relationship(
        "DataConfidence",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    next_actions = relationship(
        "NextAction",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    identities = relationship(
        "Identity",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    life_maps = relationship(
        "LifeMap",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    operating_systems = relationship(
        "OperatingSystem",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    archive_events = relationship(
        "ArchiveEvent",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    settings = relationship(
        "UserSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )


class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("users.user_id"), primary_key=True
    )
    dark_mode: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="ko", server_default="ko", nullable=False)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)
    reminder_hour: Mapped[int] = mapped_column(Integer, default=20, server_default="20", nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Seoul", server_default="Asia/Seoul", nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="settings")

class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    oauth_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(20), nullable=False)
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_email: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="oauth_accounts")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    refresh_token_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False, index=True)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    device_name: Mapped[str] = mapped_column(String(100), nullable=True)
    expired_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    last_login_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="refresh_tokens")
