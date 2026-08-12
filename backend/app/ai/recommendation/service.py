from app.schemas.recommendation import (
    RecommendationGenerateResponse,
    RecommendationCurrentResponse,
    RecommendationDetailResponse,
)


class RecommendationService:

    def __init__(
        self,
        engine,
        repository,
        pattern_repository,
        growth_repository,
        identity_repository,
        life_map_repository,
    ):
        self.engine = engine
        self.repository = repository

        self.pattern_repository = pattern_repository
        self.growth_repository = growth_repository
        self.identity_repository = identity_repository
        self.life_map_repository = life_map_repository

    # ======================================================
    # Generate Recommendation
    # ======================================================

    async def generate(
        self,
        user_id: int,
    ) -> RecommendationGenerateResponse:

        # --------------------------------------------------
        # 1. 최신 Pattern 조회
        # --------------------------------------------------

        pattern_model = (
            await self.pattern_repository.get_latest_pattern(
                user_id
            )
        )

        if pattern_model is None:
            raise ValueError(
                "사용자의 분석된 Pattern이 존재하지 않습니다."
            )

        pattern_id = pattern_model.pattern_id

        # --------------------------------------------------
        # 2. Pattern
        # --------------------------------------------------

        pattern = {
            "future_score": float(
                pattern_model.future_score or 0
            ),
            "creativity_score": float(
                pattern_model.creativity_score or 0
            ),
            "execution_score": float(
                pattern_model.execution_score or 0
            ),
            "uncertainty_score": float(
                pattern_model.uncertainty_score or 0
            ),
            "perfectionism_score": float(
                pattern_model.perfectionism_score or 0
            ),
            "resilience_score": float(
                pattern_model.resilience_score or 0
            ),
            "confidence": float(
                pattern_model.confidence or 0
            ),
            "model_version": pattern_model.model_version,
        }

        # --------------------------------------------------
        # 3. Growth
        # --------------------------------------------------

        growth_model = (
            await self.growth_repository.get_by_pattern(
                pattern_id
            )
        )

        if growth_model is None:
            raise ValueError(
                "사용자의 Growth 분석 결과가 존재하지 않습니다."
            )

        growth_items = (
            await self.growth_repository.get_growth_items(
                growth_model.growth_analysis_id
            )
        )

        growth = {
            "analysis_version": growth_model.analysis_version,
            "llm_model": growth_model.llm_model,
            "confidence": float(
                growth_model.confidence or 0
            ),
            "growth_items": [
                {
                    "title": item.title,
                    "description": item.content,
                    "priority": item.priority,
                    "type": (
                        item.growth_item_type.type_name
                        if item.growth_item_type
                        else None
                    ),
                }
                for item in growth_items
            ],
        }

        # --------------------------------------------------
        # 4. Identity
        # --------------------------------------------------

        identity_model = (
            await self.identity_repository.get_current(
                user_id
            )
        )

        if identity_model is None:
            raise ValueError(
                "사용자의 현재 Identity가 존재하지 않습니다."
            )

        keywords = (
            await self.identity_repository.get_keywords(
                identity_model.identity_id
            )
        )

        strengths = (
            await self.identity_repository.get_strengths(
                identity_model.identity_id
            )
        )

        growth_points = (
            await self.identity_repository.get_growth_points(
                identity_model.identity_id
            )
        )

        identity = {
            "identity_name": identity_model.identity_name,
            "description": identity_model.description,
            "confidence": float(
                identity_model.confidence or 0
            ),
            "version": identity_model.version,
            "keywords": keywords,
            "strengths": strengths,
            "growth_points": growth_points,
        }

        # --------------------------------------------------
        # 5. LifeMap
        # --------------------------------------------------

        life_map_model = (
            await self.life_map_repository.get_current(
                user_id
            )
        )

        if life_map_model is None:
            raise ValueError(
                "사용자의 현재 LifeMap이 존재하지 않습니다."
            )

        nodes = (
            await self.life_map_repository.get_nodes(
                life_map_model.life_map_id
            )
        )

        life_map = {
            "nodes": [
                {
                    "title": node.title,
                    "node_type": (
                        node.node_type.code
                        if node.node_type
                        else None
                    ),
                    "importance": float(
                        node.importance or 0
                    ),
                }
                for node in nodes
            ]
        }

        # --------------------------------------------------
        # 6. Recommendation Engine
        # --------------------------------------------------

        result = await self.engine.run(
            pattern,
            growth,
            identity,
            life_map,
        )

        # --------------------------------------------------
        # 7. DB Persistence
        #
        # save() 내부에서
        #
        # RecommendationGeneration
        #       ↓
        # Recommendation
        #       ↓
        # NextAction
        #
        # 순서로 저장한다.
        # --------------------------------------------------

        generation_id = await self.repository.save(
            user_id=user_id,
            pattern_id=pattern_id,
            result=result,
        )

        # --------------------------------------------------
        # 8. 방금 생성한 Generation 조회
        # --------------------------------------------------

        generation = (
            await self.repository.get_generation(
                user_id=user_id,
                generation_id=generation_id,
            )
        )

        if generation is None:
            raise ValueError(
                "Recommendation Generation 저장 후 조회에 실패했습니다."
            )

        # --------------------------------------------------
        # 9. Generate Response
        # --------------------------------------------------

        return RecommendationGenerateResponse(
            pattern_id=generation.pattern_id,
            generation_id=generation.generation_id,
            confidence=float(generation.confidence),
            version=generation.version,
            recommendations=[
                RecommendationDetailResponse.model_validate(
                    recommendation
                )
                for recommendation
                in generation.recommendations
            ],
        )

    # ======================================================
    # Current Recommendation
    # ======================================================

    async def get_current(
        self,
        user_id: int,
    ) -> RecommendationCurrentResponse:

        # --------------------------------------------------
        # 1. 최신 Pattern 조회
        # --------------------------------------------------

        pattern_model = (
            await self.pattern_repository.get_latest_pattern(
                user_id
            )
        )

        if pattern_model is None:
            raise ValueError(
                "사용자의 분석된 Pattern이 존재하지 않습니다."
            )

        # --------------------------------------------------
        # 2. 최신 Generation 조회
        # --------------------------------------------------

        generation = (
            await self.repository.get_current_generation(
                user_id=user_id,
                pattern_id=pattern_model.pattern_id,
            )
        )

        if generation is None:
            raise ValueError(
                "사용자의 Recommendation Generation이 존재하지 않습니다."
            )

        # --------------------------------------------------
        # 3. Current Response
        # --------------------------------------------------

        return RecommendationCurrentResponse(
            pattern_id=generation.pattern_id,
            generation_id=generation.generation_id,
            confidence=float(generation.confidence),
            version=generation.version,
            recommendations=[
                RecommendationDetailResponse.model_validate(
                    recommendation
                )
                for recommendation
                in generation.recommendations
            ],
        )