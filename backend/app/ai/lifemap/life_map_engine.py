from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)

from app.ai.identity.identity_result import (
    IdentityResult,
)

from app.ai.growth.growth_result import (
    GrowthResult,
)

from app.ai.lifemap.life_map_builder import (
    LifeMapBuilder,
)

from app.ai.lifemap.node_builder import (
    NodeBuilder,
)

from app.ai.lifemap.edge_builder import (
    EdgeBuilder,
)

from app.ai.lifemap.life_map_result import (
    LifeMapResult,
    LifeMapOverview,
)


class LifeMapEngine:

    def __init__(self):

        self.builder = LifeMapBuilder()

        self.node_builder = NodeBuilder()

        self.edge_builder = EdgeBuilder()

    # ======================================================
    # Analyze
    # ======================================================

    def analyze(

        self,

        feature_result: FeatureResult,

        identity_result: IdentityResult,

        growth_result: GrowthResult,

    ) -> LifeMapResult:

        # --------------------------------------------------
        # Evidence
        # --------------------------------------------------

        evidences = self.builder.build(

            feature_result=feature_result,

            identity_result=identity_result,

            growth_result=growth_result,

        )

        # --------------------------------------------------
        # Nodes
        # --------------------------------------------------

        nodes = self.node_builder.build(

            feature_result=feature_result,

            identity_result=identity_result,

            growth_result=growth_result,

        )

        # --------------------------------------------------
        # Edges
        # --------------------------------------------------

        edges = self.edge_builder.build(

            identity_result=identity_result,

        )

        # --------------------------------------------------
        # Overview
        # --------------------------------------------------

        overview = LifeMapOverview(

            total_nodes=len(nodes),

            interest_count=sum(

                node.node_type == "INTEREST"

                for node in nodes

            ),

            goal_count=sum(

                node.node_type == "GOAL"

                for node in nodes

            ),

            value_count=sum(

                node.node_type == "VALUE"

                for node in nodes

            ),

            relationship_count=sum(

                node.node_type == "RELATIONSHIP"

                for node in nodes

            ),

            career_count=sum(

                node.node_type == "CAREER"

                for node in nodes

            ),

        )

        # --------------------------------------------------
        # Result
        # --------------------------------------------------

        result = LifeMapResult(

            title="My Life Map",

            overview=overview,

            nodes=nodes,

            edges=edges,

        )

        result.metadata.update(

            {

                "engine_version": "life_map_rule_v1",

                "evidence_count": len(evidences),

                "node_count": len(nodes),

                "edge_count": len(edges),

            }

        )

        return result