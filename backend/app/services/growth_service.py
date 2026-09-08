from fastapi import HTTPException
from app.ai.growth import growth_result
from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)

from app.ai.growth.evidence_builder import (
    EvidenceBuilder,
)

from app.ai.growth.growth_engine import (
    GrowthEngine,
)

from app.ai.growth.growth_result import (
    GrowthResult,
)

from app.models.growth import (
    GrowthAnalysis,
    GrowthItem,
    AIExplanation,
    Feedback,
    NextAction,
)
from app.models.analysis import (
    Recommendation,
    RecommendationGeneration,
)
from app.schemas.feedback import (
    FeedbackRequest,
    FeedbackResponse,
)
from app.repositories.pattern_repository import PatternRepository
from app.schemas.growth_current import (
    GrowthCurrentItemResponse,
    GrowthCurrentRecommendationResponse,
    GrowthCurrentFeedbackResponse,
    GrowthCurrentMetadataResponse,
    GrowthCurrentResponse,
)

from app.schemas.growth import (
    GrowthResponse,
    UnlearningResponse,
    RelearningResponse,
    NewlearningResponse,
)

class GrowthService:

    def __init__(
        self,
        growth_repository,
        pattern_repository,
    ):

        self.growth_repository = growth_repository
        self.pattern_repository = pattern_repository
        self.evidence_builder = (
            EvidenceBuilder()
        )

        self.growth_engine = (
            GrowthEngine()
        )

    async def get_current(
        self,
        user_id: int,
    ) -> GrowthCurrentResponse:

        growth_analysis = await self.growth_repository.get_current_growth(
            user_id
        )

        if growth_analysis is None:
            raise HTTPException(status_code=404, detail="Current Growth not found.")

        recommendations = await self.growth_repository.get_recommendations(
            growth_analysis.pattern_id
        )

        feedbacks = await self.growth_repository.get_feedbacks(
            growth_analysis.growth_analysis_id
        )

        explanations = []
        for item in growth_analysis.growth_items:
            for explanation in await self.growth_repository.get_explanations(item.growth_item_id):
                explanations.append({"title": explanation.title, "content": explanation.content,
                                     "confidence": float(explanation.confidence)})
        actions = await self.growth_repository.get_actions(
            user_id, [r.recommendation_id for r in recommendations]
        )
        return GrowthCurrentResponse(
            explanations=explanations,
            actions=[{"action_id": a.action_id, "recommendation_id": a.recommendation_id,
                      "title": a.title, "description": a.description, "status": a.status}
                     for a in actions],

            items=[

                GrowthCurrentItemResponse(

                    type=item.growth_item_type.type_name,

                    title=item.title,

                    content=item.content,

                    priority=item.priority,

                )

                for item in growth_analysis.growth_items

            ],

            recommendations=[

                GrowthCurrentRecommendationResponse(
                    recommendation_id=recommendation.recommendation_id,

                    title=recommendation.title,

                    description=recommendation.description,

                    priority=recommendation.priority,

                )

                for recommendation in recommendations

            ],

            feedback=(

                GrowthCurrentFeedbackResponse(

                    rating=feedbacks[0].rating,

                    comment=feedbacks[0].comment,

                )

                if feedbacks

                else None

            ),

            metadata=GrowthCurrentMetadataResponse(

                growth_analysis_id=growth_analysis.growth_analysis_id,

                analysis_version=growth_analysis.analysis_version,

                llm_model=growth_analysis.llm_model,

                confidence=float(
                    growth_analysis.confidence
                ),

                created_at=growth_analysis.created_at,

            ),
        )



    async def submit_feedback(
        self,
        growth_analysis_id: int,
        request: FeedbackRequest,
    ) -> FeedbackResponse:

        growth_analysis = await self.growth_repository.get_growth_analysis(
            growth_analysis_id
        )

        if growth_analysis is None:
            raise ValueError(
                "Growth Analysis not found."
            )

        feedback = await self.growth_repository.upsert_feedback(
            growth_analysis_id=growth_analysis_id,
            rating=request.rating,
            comment=request.comment,
        )

        await self.growth_repository.commit()

        return FeedbackResponse(

            feedback_id=feedback.feedback_id,

            rating=feedback.rating,

            comment=feedback.comment,

            message="Feedback saved successfully.",

        )


    async def analyze(
        self,
        user_id: int,
        feature_result: FeatureResult,
        pattern_id: int,
    ):

        evidence_map = (
            self.evidence_builder.build(
                feature_result
            )
        )

        growth_result = (
            self.growth_engine.analyze(
                evidence_map
            )
        )

        growth_confidence = self._calculate_growth_confidence(
            feature_result,
            growth_result,
        )

        growth_result.metadata.setdefault(
            "confidence",
            growth_confidence,
        )

        growth_analysis = GrowthAnalysis(
            pattern_id=pattern_id,
            analysis_version=str(
                growth_result.metadata.get(
                    "engine_version",
                    "rule_v1",
                )
            ),
            llm_model=str(
                growth_result.metadata.get(
                    "llm_model",
                    "rule_engine",
                )
            ),
            confidence=float(
                growth_result.metadata.get(
                    "confidence",
                    0.0,
                )
            ),
        )

        await self.growth_repository.create_growth_analysis(
            growth_analysis
        )

        growth_result.metadata["growth_analysis_id"] = growth_analysis.growth_analysis_id

        created_items: list[GrowthItem] = []

        items = [
            ("UNLEARNING", growth_result.unlearning),
            ("RELEARNING", growth_result.relearning),
            ("NEWLEARNING", growth_result.newlearning),
        ]

        for type_name, item_data in items:

            if item_data is None:
                continue

            item_type = await self.growth_repository.get_or_create_growth_item_type(
                type_name=type_name,
                display_order=1,
            )

            growth_item = GrowthItem(
                growth_analysis_id=growth_analysis.growth_analysis_id,
                type_id=item_type.type_id,
                title=item_data.get("title", ""),
                content=item_data.get("description", ""),
                priority=int(
                    item_data.get("priority", 1)
                ),
            )

            created_item = await self.growth_repository.create_growth_item(
                growth_item
            )

            created_items.append(created_item)

        await self._persist_explanations(
            growth_result,
            created_items,
        )

        await self._persist_feedback(
            growth_result,
            growth_analysis,
        )

        await self._persist_recommendations(
            user_id=user_id,
            pattern_id=pattern_id,
            confidence=float(growth_analysis.confidence),
            growth_result=growth_result,
        )

        # Ensure confidence fields exist for Pydantic validation
        def _ensure_confidence(item):
            if not item:
                return None
            if "confidence" not in item or item.get("confidence") is None:
                item["confidence"] = 0.0
            return item

        un = _ensure_confidence(growth_result.unlearning)
        re = _ensure_confidence(growth_result.relearning)
        ne = _ensure_confidence(growth_result.newlearning)

        return GrowthResponse(
            unlearning=(
                UnlearningResponse(
                    **un
                )
                if un
                else None
            ),
            relearning=(
                RelearningResponse(
                    **re
                )
                if re
                else None
            ),
            newlearning=(
                NewlearningResponse(
                    **ne
                )
                if ne
                else None
            ),
            explanations=growth_result.explanations,
            recommendations=growth_result.recommendations,
            feedback=growth_result.feedback,
            metadata=growth_result.metadata,
            warnings=growth_result.warnings,
        )

    def _calculate_growth_confidence(
        self,
        feature_result: FeatureResult,
        growth_result: GrowthResult,
    ) -> float:
        item_confidences = [
            float(item.get("confidence") or 0.0)
            for item in (
                growth_result.unlearning,
                growth_result.relearning,
                growth_result.newlearning,
            )
            if item is not None
        ]

        if item_confidences:
            return round(
                sum(item_confidences)
                /
                len(item_confidences),
                2,
            )

        return float(feature_result.confidence_score)

    async def _persist_recommendations(
        self,
        user_id: int,
        pattern_id: int,
        confidence: float,
        growth_result: GrowthResult,
    ) -> None:
        if not growth_result.recommendations:
            return

        generation = await self.growth_repository.create_recommendation_generation(
            RecommendationGeneration(
                pattern_id=pattern_id,
                confidence=confidence,
                version=str(
                    growth_result.metadata.get(
                        "engine_version",
                        "growth_rule_v1",
                    )
                ),
            )
        )

        for recommendation_data in growth_result.recommendations:
            recommendation = await self.growth_repository.create_recommendation(
                Recommendation(
                    generation_id=generation.generation_id,
                    pattern_id=pattern_id,
                    title=recommendation_data.get(
                        "title",
                        "성장 제안",
                    ),
                    description=recommendation_data.get(
                        "description"
                    ),
                    priority=int(
                        recommendation_data.get(
                            "priority",
                            1,
                        )
                    ),
                    status="WAITING",
                )
            )

            await self.growth_repository.create_next_action(
                NextAction(
                    user_id=user_id,
                    recommendation_id=recommendation.recommendation_id,
                    title=recommendation.title,
                    description=recommendation.description,
                    status="WAITING",
                )
            )

    async def _persist_explanations(
        self,
        growth_result: GrowthResult,
        created_items: list[GrowthItem],
    ) -> None:

        if not growth_result.explanations:
            return

        for explanation_data in growth_result.explanations:
            explanation_type = await self.growth_repository.get_or_create_explanation_type(
                type_code=explanation_data.get("type", "DEFAULT"),
                type_name=explanation_data.get("type", "Explanation"),
                display_order=int(
                    explanation_data.get("display_order", 1)
                ),
            )

            target_item = None
            if len(created_items) == 1:
                target_item = created_items[0]
            elif len(created_items) > 1:
                target_item = created_items[0]

            if target_item is None:
                continue

            await self.growth_repository.create_ai_explanation(
                AIExplanation(
                    growth_item_id=target_item.growth_item_id,
                    type_id=explanation_type.type_id,
                    title=explanation_data.get("title", "설명"),
                    content=explanation_data.get("content", ""),
                    confidence=float(
                        explanation_data.get("confidence") or 0.0
                    ),
                    display_order=int(
                        explanation_data.get("display_order", 1)
                    ),
                )
            )



    async def _persist_feedback(
        self,
        growth_result: GrowthResult,
        growth_analysis: GrowthAnalysis,
    ) -> None:

        if not growth_result.feedback:
            return

        await self.growth_repository.create_feedback(
            Feedback(
                growth_analysis_id=growth_analysis.growth_analysis_id,
                rating=int(
                    growth_result.feedback.get("rating", 0)
                ),
                comment=growth_result.feedback.get("comment"),
            )
        )
