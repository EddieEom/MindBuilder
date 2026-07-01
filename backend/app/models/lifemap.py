# backend/app/models/lifemap.py

from sqlalchemy import (
    BIGINT,
    SMALLINT,
    INTEGER,
    DECIMAL,
    String,
    TIMESTAMP,
    ForeignKey,
    func,
    CheckConstraint
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# ==========================================================
# Life Map
# ==========================================================

class LifeMap(Base):
    __tablename__ = "life_maps"

    life_map_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("users.user_id"),
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

    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="life_maps",
    )

    nodes = relationship(
        "LifeMapNode",
        back_populates="life_map",
        cascade="all, delete-orphan",
    )

    edges = relationship(
        "LifeMapEdge",
        back_populates="life_map",
        cascade="all, delete-orphan",
    )

    operating_systems = relationship(
        "OperatingSystem",
        back_populates="life_map",
    )


# ==========================================================
# Node Type
# ==========================================================

class NodeType(Base):
    __tablename__ = "node_types"

    node_type_id: Mapped[int] = mapped_column(
        SMALLINT,
        primary_key=True,
        autoincrement=True,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Relationships

    nodes = relationship(
        "LifeMapNode",
        back_populates="node_type",
    )


# ==========================================================
# Life Map Node
# ==========================================================

class LifeMapNode(Base):
    __tablename__ = "life_map_nodes"

    node_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    life_map_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("life_maps.life_map_id"),
        nullable=False,
    )

    node_type_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey("node_types.node_type_id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    importance: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        server_default="0",
        nullable=False,
    )

    x_position: Mapped[float | None] = mapped_column(
        DECIMAL(8, 2),
        nullable=True,
    )

    y_position: Mapped[float | None] = mapped_column(
        DECIMAL(8, 2),
        nullable=True,
    )

    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    # Relationships

    life_map = relationship(
        "LifeMap",
        back_populates="nodes",
    )

    node_type = relationship(
        "NodeType",
        back_populates="nodes",
    )

    outgoing_edges = relationship(
        "LifeMapEdge",
        foreign_keys="LifeMapEdge.from_node_id",
        back_populates="from_node",
        cascade="all, delete-orphan",
    )

    incoming_edges = relationship(
        "LifeMapEdge",
        foreign_keys="LifeMapEdge.to_node_id",
        back_populates="to_node",
        cascade="all, delete-orphan",
    )

    node_tags = relationship(
        "NodeTag",
        back_populates="node",
        cascade="all, delete-orphan",
    )

    goals = relationship(
        "Goal",
        back_populates="node",
        cascade="all, delete-orphan",
    )


# ==========================================================
# Edge Type
# ==========================================================

class EdgeType(Base):
    __tablename__ = "edge_types"

    edge_type_id: Mapped[int] = mapped_column(
        SMALLINT,
        primary_key=True,
        autoincrement=True,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Relationships

    edges = relationship(
        "LifeMapEdge",
        back_populates="edge_type",
    )


# ==========================================================
# Life Map Edge
# ==========================================================

class LifeMapEdge(Base):
    __tablename__ = "life_map_edges"

    edge_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    life_map_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("life_maps.life_map_id"),
        nullable=False,
    )

    from_node_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("life_map_nodes.node_id"),
        nullable=False,
    )

    to_node_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("life_map_nodes.node_id"),
        nullable=False,
    )

    edge_type_id: Mapped[int] = mapped_column(
        SMALLINT,
        ForeignKey("edge_types.edge_type_id"),
        nullable=False,
    )

    weight: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        server_default="1",
        nullable=False,
    )

    # Relationships

    life_map = relationship(
        "LifeMap",
        back_populates="edges",
    )

    edge_type = relationship(
        "EdgeType",
        back_populates="edges",
    )

    from_node = relationship(
        "LifeMapNode",
        foreign_keys=[from_node_id],
        back_populates="outgoing_edges",
    )

    to_node = relationship(
        "LifeMapNode",
        foreign_keys=[to_node_id],
        back_populates="incoming_edges",
    )


# ==========================================================
# Tag
# ==========================================================

class Tag(Base):
    __tablename__ = "tags"

    tag_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    # Relationships

    node_tags = relationship(
        "NodeTag",
        back_populates="tag",
        cascade="all, delete-orphan",
    )


# ==========================================================
# Node Tag
# ==========================================================

class NodeTag(Base):
    __tablename__ = "node_tags"

    node_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("life_map_nodes.node_id"),
        primary_key=True,
    )

    tag_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("tags.tag_id"),
        primary_key=True,
    )

    # Relationships

    node = relationship(
        "LifeMapNode",
        back_populates="node_tags",
    )

    tag = relationship(
        "Tag",
        back_populates="node_tags",
    )


# ==========================================================
# Goal
# ==========================================================

class Goal(Base):
    __tablename__ = "goals"

    __table_args__ = (
        CheckConstraint(
            "status IN ('IN_PROGRESS', 'COMPLETED', 'FAILED')",
            name="ck_goal_status",
        ),
    )

    goal_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

    node_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("life_map_nodes.node_id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    progress: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        server_default="0",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        server_default="IN_PROGRESS",
        nullable=False,
    )

    # Relationships

    node = relationship(
        "LifeMapNode",
        back_populates="goals",
    )