from dataclasses import dataclass, field

# ==========================================================
# Node Tag
# ==========================================================


@dataclass
class NodeTag:

    name: str


# ==========================================================
# Related Goal
# ==========================================================


@dataclass
class RelatedGoal:

    title: str

    progress: int


# ==========================================================
# Life Map Node
# ==========================================================


@dataclass
class LifeMapNode:

    node_id: str

    title: str

    node_type: str

    importance: float

    x: float = 0.0

    y: float = 0.0

    color: str = ""

    icon: str = ""

    tags: list[NodeTag] = field(default_factory=list)

    summary: str = ""

    related_goals: list[RelatedGoal] = field(default_factory=list)


# ==========================================================
# Edge
# ==========================================================


@dataclass
class LifeMapEdge:

    from_node: str

    to_node: str

    edge_type: str

    weight: float


# ==========================================================
# Overview
# ==========================================================


@dataclass
class LifeMapOverview:

    total_nodes: int = 0

    interest_count: int = 0

    goal_count: int = 0

    value_count: int = 0

    relationship_count: int = 0

    career_count: int = 0


# ==========================================================
# LifeMap Result
# ==========================================================


@dataclass
class LifeMapResult:

    title: str

    overview: LifeMapOverview

    nodes: list[LifeMapNode] = field(default_factory=list)

    edges: list[LifeMapEdge] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    warnings: list[str] = field(default_factory=list)
