from typing import Any, Awaitable, Callable, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.feature_extractor.constants import (
    CREATIVITY,
    EXECUTION,
    FUTURE,
    PERFECTIONISM,
    RESILIENCE,
    UNCERTAINTY,
)
from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)
from app.ai.growth.growth_result import (
    GrowthResult,
)
from app.ai.identity.identity_result import (
    IdentityResult,
)
from app.ai.lifemap.life_map_engine import (
    LifeMapEngine,
)
from app.ai.lifemap.life_map_result import (
    LifeMapResult,
)
from app.models.analysis import (
    PatternAnalysis,
)
from app.models.lifemap import (
    Goal,
    LifeMap,
    LifeMapEdge,
    LifeMapNode,
    NodeTag,
)
from app.repositories.feature_repository import (
    FeatureRepository,
)
from app.repositories.growth_repository import (
    GrowthRepository,
)
from app.repositories.identity_repository import (
    IdentityRepository,
)
from app.repositories.life_map_repository import (
    LifeMapRepository,
)
from app.repositories.pattern_repository import (
    PatternRepository,
)
from app.schemas.lifemap import (
    LifeMapEdgeResponse,
    LifeMapNodeResponse,
    LifeMapOverviewResponse,
    LifeMapResponse,
    NodeGoalResponse,
    NodeTagResponse,
)


FeatureGetter = Callable[[int], Awaitable[FeatureResult]]


class LifeMapService:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.feature_repository = FeatureRepository(db)

        self.pattern_repository = PatternRepository(db)

        self.identity_repository = IdentityRepository(db)

        self.growth_repository = GrowthRepository(db)

        self.life_map_repository = LifeMapRepository(db)

        self.life_map_engine = LifeMapEngine()

    # ======================================================
    # Analyze
    # ======================================================

    async def analyze(
        self,
        user_id: int,
    ) -> LifeMapResponse:

        latest_pattern = await self._get_latest_pattern(
            user_id
        )

        feature_result = await self._get_latest_feature_result(
            user_id=user_id,
            latest_pattern=latest_pattern,
        )

        identity_result = await self._get_current_identity_result(
            user_id=user_id,
            latest_pattern=latest_pattern,
        )

        growth_result = await self._get_current_growth_result(
            latest_pattern
        )

        life_map_result = self.life_map_engine.analyze(
            feature_result=feature_result,
            identity_result=identity_result,
            growth_result=growth_result,
        )

        life_map = await self._save_result(
            user_id=user_id,
            result=life_map_result,
        )

        nodes = await self.life_map_repository.get_nodes(
            life_map.life_map_id
        )

        edges = await self.life_map_repository.get_edges(
            life_map.life_map_id
        )

        return self._model_to_response(
            life_map=life_map,
            nodes=nodes,
            edges=edges,
            title=life_map_result.title,
            metadata=life_map_result.metadata,
            warnings=life_map_result.warnings,
        )

    async def _get_latest_pattern(
        self,
        user_id: int,
    ) -> PatternAnalysis:

        pattern = await self.pattern_repository.get_latest_pattern(
            user_id
        )

        if pattern is None:

            raise ValueError(
                "Latest Pattern not found. LifeMap requires Layer2 Pattern data."
            )

        return pattern

    async def _get_latest_feature_result(
        self,
        user_id: int,
        latest_pattern: PatternAnalysis,
    ) -> FeatureResult:

        getter = getattr(
            self.feature_repository,
            "get_latest_feature_result",
            None,
        )

        if getter is not None:

            typed_getter = cast(
                FeatureGetter,
                getter,
            )

            return await typed_getter(
                user_id
            )

        # TODO:
        # FeatureRepository.get_latest_feature_result(user_id) should return
        # the latest persisted FeatureResult. Until that repository method is
        # added, LifeMap uses the latest Layer2 Pattern scores as the stable
        # feature source because PatternAnalysis is generated from FeatureResult.
        return self._feature_result_from_pattern(
            latest_pattern
        )

    async def _get_current_identity_result(
        self,
        user_id: int,
        latest_pattern: PatternAnalysis,
    ) -> IdentityResult:

        identity = await self.identity_repository.get_current(
            user_id
        )

        if identity is None:

            raise ValueError(
                "Current Identity not found. LifeMap requires Layer3 Identity data."
            )

        keywords = await self.identity_repository.get_keywords(
            identity.identity_id
        )

        strengths = await self.identity_repository.get_strengths(
            identity.identity_id
        )

        growth_points = await self.identity_repository.get_growth_points(
            identity.identity_id
        )

        result = IdentityResult()

        result.set_identity(
            identity_name=identity.identity_name,
            description=identity.description or "",
            confidence=float(
                identity.confidence
            ),
        )

        result.set_scores(
            creativity=int(
                round(
                    float(
                        latest_pattern.creativity_score
                    )
                )
            ),
            execution=int(
                round(
                    float(
                        latest_pattern.execution_score
                    )
                )
            ),
            uncertainty=int(
                round(
                    float(
                        latest_pattern.uncertainty_score
                    )
                )
            ),
        )

        for keyword in keywords:

            result.add_keyword(
                keyword
            )

        for strength in strengths:

            result.add_strength(
                strength
            )

        for growth_point in growth_points:

            result.add_growth_point(
                growth_point
            )

        result.set_metadata(
            "identity_id",
            identity.identity_id,
        )

        result.set_metadata(
            "version",
            identity.version,
        )

        result.set_metadata(
            "generated_at",
            identity.generated_at,
        )

        return result

    async def _get_current_growth_result(
        self,
        latest_pattern: PatternAnalysis,
    ) -> GrowthResult:

        growth_analysis = await self.growth_repository.get_by_pattern(
            latest_pattern.pattern_id
        )

        if growth_analysis is None:

            raise ValueError(
                "Current Growth not found. LifeMap requires Growth data."
            )

        growth_items = await self.growth_repository.get_growth_items(
            growth_analysis.growth_analysis_id
        )

        result = GrowthResult()

        result.set_metadata(
            "growth_analysis_id",
            growth_analysis.growth_analysis_id,
        )

        result.set_metadata(
            "pattern_id",
            growth_analysis.pattern_id,
        )

        result.set_metadata(
            "analysis_version",
            growth_analysis.analysis_version,
        )

        result.set_metadata(
            "llm_model",
            growth_analysis.llm_model,
        )

        result.set_metadata(
            "confidence",
            float(
                growth_analysis.confidence
            ),
        )

        for item in growth_items:

            result.add_explanation(
                {
                    "growth_item_id": item.growth_item_id,
                    "title": item.title,
                    "content": item.content,
                    "priority": item.priority,
                }
            )

        return result

    def _feature_result_from_pattern(
        self,
        pattern: PatternAnalysis,
    ) -> FeatureResult:

        result = FeatureResult()

        result.scores.update(
            {
                FUTURE: float(
                    pattern.future_score
                ),
                CREATIVITY: float(
                    pattern.creativity_score
                ),
                EXECUTION: float(
                    pattern.execution_score
                ),
                UNCERTAINTY: float(
                    pattern.uncertainty_score
                ),
                PERFECTIONISM: float(
                    pattern.perfectionism_score
                ),
                RESILIENCE: float(
                    pattern.resilience_score
                ),
            }
        )

        result.confidence_score = int(
            round(
                float(
                    pattern.confidence
                )
            )
        )

        result.metadata.update(
            {
                "source_layer": "Layer2",
                "source": "latest_pattern",
                "pattern_id": pattern.pattern_id,
                "scan_id": pattern.scan_id,
            }
        )

        return result

    async def _save_result(
        self,
        user_id: int,
        result: LifeMapResult,
    ) -> LifeMap:

        life_map = await self.life_map_repository.create(
            LifeMap(
                user_id=user_id,
                version=1,
            )
        )

        node_lookup: dict[str, LifeMapNode] = {}

        for node_result in result.nodes:

            node_type = (
                await self.life_map_repository.get_or_create_node_type(
                    node_result.node_type
                )
            )

            node = LifeMapNode(
                life_map_id=life_map.life_map_id,
                node_type_id=node_type.node_type_id,
                title=self._limit_text(
                    node_result.title,
                    100,
                ),
                importance=node_result.importance,
                x_position=node_result.x,
                y_position=node_result.y,
            )

            saved_node = await self.life_map_repository.create_node(
                node
            )

            node_lookup[node_result.node_id] = saved_node

            for tag_result in node_result.tags:

                tag = await self.life_map_repository.get_or_create_tag(
                    tag_result.name
                )

                await self.life_map_repository.create_node_tag(
                    NodeTag(
                        node_id=saved_node.node_id,
                        tag_id=tag.tag_id,
                    )
                )

            for goal_result in node_result.related_goals:

                await self.life_map_repository.create_goal(
                    Goal(
                        node_id=saved_node.node_id,
                        title=goal_result.title,
                        progress=goal_result.progress,
                        status="IN_PROGRESS",
                    )
                )

        for edge_result in result.edges:

            from_node = node_lookup.get(
                edge_result.from_node
            )

            to_node = node_lookup.get(
                edge_result.to_node
            )

            if from_node is None or to_node is None:

                result.warnings.append(
                    (
                        "LifeMap edge skipped because node was not found: "
                        f"{edge_result.from_node} -> {edge_result.to_node}"
                    )
                )

                continue

            edge_type = (
                await self.life_map_repository.get_or_create_edge_type(
                    edge_result.edge_type
                )
            )

            await self.life_map_repository.create_edge(
                LifeMapEdge(
                    life_map_id=life_map.life_map_id,
                    from_node_id=from_node.node_id,
                    to_node_id=to_node.node_id,
                    edge_type_id=edge_type.edge_type_id,
                    weight=edge_result.weight,
                )
            )

        await self.life_map_repository.commit()

        return life_map

    # ======================================================
    # Current LifeMap
    # ======================================================

    async def get_current(
        self,
        user_id: int,
    ) -> LifeMapResponse:

        life_map = await self.life_map_repository.get_current(
            user_id
        )

        if life_map is None:

            return LifeMapResponse(
                title="",
                overview=self._overview_response(
                    nodes=[],
                    edges=[],
                ),
                nodes=[],
                edges=[],
                metadata={},
                warnings=[],
            )

        nodes = await self.life_map_repository.get_nodes(
            life_map.life_map_id
        )

        edges = await self.life_map_repository.get_edges(
            life_map.life_map_id
        )

        return self._model_to_response(
            life_map=life_map,
            nodes=nodes,
            edges=edges,
            title="My Life Map",
            metadata={},
            warnings=[],
        )

    # ======================================================
    # Model -> Response
    # ======================================================

    def _model_to_response(
        self,
        life_map: LifeMap,
        nodes: list[LifeMapNode],
        edges: list[LifeMapEdge],
        title: str,
        metadata: dict[str, Any],
        warnings: list[str],
    ) -> LifeMapResponse:

        return LifeMapResponse(
            title=title,
            overview=self._overview_response(
                nodes=nodes,
                edges=edges,
            ),
            nodes=[
                self._node_model_to_response(
                    node
                )
                for node in nodes
            ],
            edges=[
                self._edge_model_to_response(
                    edge
                )
                for edge in edges
            ],
            metadata={
                **metadata,
                "life_map_id": life_map.life_map_id,
                "version": life_map.version,
                "generated_at": life_map.generated_at,
            },
            warnings=warnings,
        )

    def _overview_response(
        self,
        nodes: list[LifeMapNode],
        edges: list[LifeMapEdge],
    ) -> LifeMapOverviewResponse:

        def count_node_type(
            node_type: str,
        ) -> int:

            return sum(
                node.node_type.code == node_type
                for node in nodes
            )

        return LifeMapOverviewResponse(
            total_nodes=len(nodes),
            interest_count=count_node_type(
                "INTEREST"
            ),
            goal_count=count_node_type(
                "GOAL"
            ),
            value_count=count_node_type(
                "VALUE"
            ),
            connection_count=len(edges),
        )

    def _node_model_to_response(
        self,
        node: LifeMapNode,
    ) -> LifeMapNodeResponse:

        node_type = node.node_type.code

        color, icon = self._style_for_node_type(
            node_type
        )

        return LifeMapNodeResponse(
            node_id=str(
                node.node_id
            ),
            title=node.title,
            node_type=node_type,
            importance=float(
                node.importance
            ),
            color=color,
            icon=icon,
            summary="",
            x=float(
                node.x_position
                or
                0.0
            ),
            y=float(
                node.y_position
                or
                0.0
            ),
            tags=[
                NodeTagResponse(
                    name=node_tag.tag.name
                )
                for node_tag in node.node_tags
            ],
            related_goals=[
                NodeGoalResponse(
                    title=goal.title,
                    progress=float(
                        goal.progress
                    ),
                    status=goal.status,
                )
                for goal in node.goals
            ],
        )

    def _edge_model_to_response(
        self,
        edge: LifeMapEdge,
    ) -> LifeMapEdgeResponse:

        return LifeMapEdgeResponse(
            from_node=str(
                edge.from_node.node_id
            ),
            to_node=str(
                edge.to_node.node_id
            ),
            edge_type=edge.edge_type.code,
            weight=float(
                edge.weight
            ),
        )

    def _style_for_node_type(
        self,
        node_type: str,
    ) -> tuple[str, str]:

        styles = {
            "IDENTITY": ("#4F6BFF", "person"),
            "INTEREST": ("#8BD17C", "tag"),
            "GOAL": ("#FFA94D", "flag"),
            "VALUE": ("#9B8AFB", "star"),
            "RELATIONSHIP": ("#4DABF7", "link"),
            "CAREER": ("#15AABF", "briefcase"),
        }

        return styles.get(
            node_type,
            ("#ADB5BD", "circle"),
        )

    def _limit_text(
        self,
        value: str,
        max_length: int,
    ) -> str:

        if len(value) <= max_length:

            return value

        return value[
            : max_length - 3
        ] + "..."
