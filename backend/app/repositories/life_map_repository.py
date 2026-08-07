from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.lifemap import (
    EdgeType,
    Goal,
    LifeMap,
    LifeMapEdge,
    LifeMapNode,
    NodeTag,
    NodeType,
    Tag,
)


class LifeMapRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.db = db

    # ======================================================
    # LifeMap
    # ======================================================

    async def create(
        self,
        life_map: LifeMap,
    ) -> LifeMap:

        self.db.add(life_map)

        await self.db.flush()

        await self.db.refresh(life_map)

        return life_map

    async def get_current(
        self,
        user_id: int,
    ) -> LifeMap | None:

        stmt = (
            select(LifeMap)
            .where(
                LifeMap.user_id == user_id
            )
            .order_by(
                LifeMap.generated_at.desc(),
                LifeMap.life_map_id.desc(),
            )
            .limit(1)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    # ======================================================
    # Node Type
    # ======================================================

    async def get_or_create_node_type(
        self,
        code: str,
    ) -> NodeType:

        normalized_code = code.upper()

        stmt = (
            select(NodeType)
            .where(
                NodeType.code == normalized_code
            )
        )

        result = await self.db.execute(stmt)

        node_type = result.scalar_one_or_none()

        if node_type is not None:

            return node_type

        node_type = NodeType(
            code=normalized_code,
            name=normalized_code.title(),
        )

        self.db.add(node_type)

        await self.db.flush()

        await self.db.refresh(node_type)

        return node_type

    # ======================================================
    # Node
    # ======================================================

    async def create_node(
        self,
        node: LifeMapNode,
    ) -> LifeMapNode:

        self.db.add(node)

        await self.db.flush()

        await self.db.refresh(node)

        return node

    async def get_nodes(
        self,
        life_map_id: int,
    ) -> list[LifeMapNode]:

        stmt = (
            select(LifeMapNode)
            .where(
                LifeMapNode.life_map_id == life_map_id
            )
            .options(
                selectinload(LifeMapNode.node_type),
                selectinload(LifeMapNode.node_tags).selectinload(
                    NodeTag.tag
                ),
                selectinload(LifeMapNode.goals),
            )
            .order_by(
                LifeMapNode.node_id.asc()
            )
        )

        result = await self.db.execute(stmt)

        return list(
            result.scalars().all()
        )

    # ======================================================
    # Edge Type
    # ======================================================

    async def get_or_create_edge_type(
        self,
        code: str,
    ) -> EdgeType:

        normalized_code = code.upper()

        stmt = (
            select(EdgeType)
            .where(
                EdgeType.code == normalized_code
            )
        )

        result = await self.db.execute(stmt)

        edge_type = result.scalar_one_or_none()

        if edge_type is not None:

            return edge_type

        edge_type = EdgeType(
            code=normalized_code,
            name=normalized_code.title(),
        )

        self.db.add(edge_type)

        await self.db.flush()

        await self.db.refresh(edge_type)

        return edge_type

    # ======================================================
    # Edge
    # ======================================================

    async def create_edge(
        self,
        edge: LifeMapEdge,
    ) -> LifeMapEdge:

        self.db.add(edge)

        await self.db.flush()

        await self.db.refresh(edge)

        return edge

    async def get_edges(
        self,
        life_map_id: int,
    ) -> list[LifeMapEdge]:

        stmt = (
            select(LifeMapEdge)
            .where(
                LifeMapEdge.life_map_id == life_map_id
            )
            .options(
                selectinload(LifeMapEdge.edge_type),
                selectinload(LifeMapEdge.from_node),
                selectinload(LifeMapEdge.to_node),
            )
            .order_by(
                LifeMapEdge.edge_id.asc()
            )
        )

        result = await self.db.execute(stmt)

        return list(
            result.scalars().all()
        )

    # ======================================================
    # Tag
    # ======================================================

    async def get_or_create_tag(
        self,
        name: str,
    ) -> Tag:

        stmt = (
            select(Tag)
            .where(
                Tag.name == name
            )
        )

        result = await self.db.execute(stmt)

        tag = result.scalar_one_or_none()

        if tag is not None:

            return tag

        tag = Tag(
            name=name
        )

        self.db.add(tag)

        await self.db.flush()

        await self.db.refresh(tag)

        return tag

    async def create_node_tag(
        self,
        node_tag: NodeTag,
    ) -> None:

        self.db.add(node_tag)

    # ======================================================
    # Goal
    # ======================================================

    async def create_goal(
        self,
        goal: Goal,
    ) -> None:

        self.db.add(goal)

    # ======================================================
    # Transaction
    # ======================================================

    async def commit(
        self,
    ) -> None:

        await self.db.commit()

    async def rollback(
        self,
    ) -> None:

        await self.db.rollback()

    # ======================================================
    # History
    # ======================================================

    async def get_history(
        self,
        user_id: int,
    ) -> list[LifeMap]:

        stmt = (
            select(LifeMap)
            .where(
                LifeMap.user_id == user_id
            )
            .order_by(
                LifeMap.generated_at.desc(),
                LifeMap.life_map_id.desc(),
            )
        )

        result = await self.db.execute(stmt)

        return list(
            result.scalars().all()
        )


    # ======================================================
    # Node
    # ======================================================

    async def get_node(
        self,
        node_id: int,
    ) -> LifeMapNode | None:

        stmt = (
            select(LifeMapNode)
            .where(
                LifeMapNode.node_id == node_id
            )
            .options(
                selectinload(
                    LifeMapNode.node_type
                ),
                selectinload(
                    LifeMapNode.node_tags
                ).selectinload(
                    NodeTag.tag
                ),
                selectinload(
                    LifeMapNode.goals
                ),
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()