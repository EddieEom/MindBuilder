from app.ai.identity.identity_result import (
    IdentityResult,
)

from app.ai.lifemap.life_map_result import (
    LifeMapEdge,
)


class EdgeBuilder:

    # ======================================================
    # Build Edge
    # ======================================================

    def build(

        self,

        identity_result: IdentityResult,

    ) -> list[LifeMapEdge]:

        edges: list[LifeMapEdge] = []

        # --------------------------------------------------
        # Root -> Keyword
        # --------------------------------------------------

        for keyword in identity_result.keywords:

            edges.append(

                LifeMapEdge(

                    from_node="ME",

                    to_node=f"KW_{keyword}",

                    edge_type="INTEREST",

                    weight=1.0,

                )

            )

        # --------------------------------------------------
        # Root -> Strength
        # --------------------------------------------------

        for strength in identity_result.strengths:

            edges.append(

                LifeMapEdge(

                    from_node="ME",

                    to_node=f"ST_{hash(strength)}",

                    edge_type="VALUE",

                    weight=0.9,

                )

            )

        # --------------------------------------------------
        # Root -> Growth Point
        # --------------------------------------------------

        for point in identity_result.growth_points:

            edges.append(

                LifeMapEdge(

                    from_node="ME",

                    to_node=f"GP_{hash(point)}",

                    edge_type="GOAL",

                    weight=0.8,

                )

            )

        return edges