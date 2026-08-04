from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)

from app.ai.identity.identity_result import (
    IdentityResult,
)

from app.ai.growth.growth_result import (
    GrowthResult,
)

from app.ai.lifemap.life_map_result import (
    LifeMapNode,
    NodeTag,
    RelatedGoal,
)


class NodeBuilder:

    # ======================================================
    # Build Nodes
    # ======================================================

    def build(

        self,

        feature_result: FeatureResult,

        identity_result: IdentityResult,

        growth_result: GrowthResult,

    ) -> list[LifeMapNode]:

        nodes: list[LifeMapNode] = []

        # --------------------------------------------------
        # Root Node
        # --------------------------------------------------

        nodes.append(

            LifeMapNode(

                node_id="ME",

                title="나",

                node_type="IDENTITY",

                importance=100,

                color="#4F6BFF",

                icon="person",

                summary=identity_result.description,

            )

        )

        # --------------------------------------------------
        # Identity Keywords
        # --------------------------------------------------

        for keyword in identity_result.keywords:

            nodes.append(

                LifeMapNode(

                    node_id=f"KW_{keyword}",

                    title=keyword,

                    node_type="INTEREST",

                    importance=75,

                    color="#8BD17C",

                    icon="tag",

                    tags=[

                        NodeTag(

                            name="Identity"

                        )

                    ],

                )

            )

        # --------------------------------------------------
        # Growth Point
        # --------------------------------------------------

        for point in identity_result.growth_points:

            nodes.append(

                LifeMapNode(

                    node_id=f"GP_{hash(point)}",

                    title=point,

                    node_type="GOAL",

                    importance=70,

                    color="#FFA94D",

                    icon="flag",

                    related_goals=[

                        RelatedGoal(

                            title=point,

                            progress=0,

                        )

                    ],

                )

            )

        # --------------------------------------------------
        # Strength
        # --------------------------------------------------

        for strength in identity_result.strengths:

            nodes.append(

                LifeMapNode(

                    node_id=f"ST_{hash(strength)}",

                    title=strength,

                    node_type="VALUE",

                    importance=65,

                    color="#9B8AFB",

                    icon="star",

                )

            )

        return nodes