from datetime import datetime

from pydantic import BaseModel, Field


# ======================================================
# Tag
# ======================================================

class NodeTagResponse(BaseModel):

    name: str


# ======================================================
# Goal
# ======================================================

class NodeGoalResponse(BaseModel):

    title: str

    progress: float

    status: str


# ======================================================
# Node
# ======================================================

class LifeMapNodeResponse(BaseModel):

    node_id: str

    title: str

    node_type: str

    importance: float

    color: str

    icon: str

    summary: str

    x: float

    y: float

    tags: list[NodeTagResponse] = Field(default_factory=list)

    related_goals: list[NodeGoalResponse] = Field(default_factory=list)


# ======================================================
# Edge
# ======================================================

class LifeMapEdgeResponse(BaseModel):

    from_node: str

    to_node: str

    edge_type: str

    weight: float


# ======================================================
# Overview
# ======================================================

class LifeMapOverviewResponse(BaseModel):

    total_nodes: int

    interest_count: int

    goal_count: int

    value_count: int

    connection_count: int


# ======================================================
# Response
# ======================================================

class LifeMapResponse(BaseModel):

    title: str

    overview: LifeMapOverviewResponse

    nodes: list[LifeMapNodeResponse]

    edges: list[LifeMapEdgeResponse]

    metadata: dict = Field(default_factory=dict)

    warnings: list[str] = Field(default_factory=list)
