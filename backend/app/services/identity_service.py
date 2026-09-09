from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.feature_extractor.constants import (
    CREATIVITY,
    EXECUTION,
    UNCERTAINTY,
)
from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)
from app.ai.identity.identity_builder import (
    IdentityBuilder,
)
from app.ai.identity.identity_engine import (
    IdentityEngine,
)
from app.models.identity import (
    Identity,
)
from app.repositories.identity_repository import (
    IdentityRepository,
)
from app.repositories.pattern_repository import (
    PatternRepository,
)
from app.schemas.growth import GrowthResponse
from app.schemas.identity import (
    IdentityResponse,
    IdentityFeedbackRequest,
    IdentityFeedbackResponse,
)


from app.schemas.identity_history import (
    IdentityHistoryItemResponse,
    IdentityHistoryResponse,
)

class IdentityService:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.identity_repository = IdentityRepository(db)

        self.pattern_repository = PatternRepository(db)

        self.identity_builder = IdentityBuilder()

        self.identity_engine = IdentityEngine()

    # ======================================================
    # Identity Analyze
    # ======================================================

    async def analyze(
        self,
        user_id: int,
        feature_result: FeatureResult,
        growth_result: GrowthResponse,
    ) -> IdentityResponse:

        latest_pattern = await self.pattern_repository.get_latest_pattern(
            user_id
        )

        recent_patterns = await self.pattern_repository.get_recent_patterns(
            user_id
        )

        pattern_average = await self.pattern_repository.get_pattern_average(
            user_id
        )

        pattern_trend = await self.pattern_repository.get_pattern_trend(
            user_id
        )

        pattern_count = await self.pattern_repository.get_pattern_count(
            user_id
        )

        evidence = self.identity_builder.build(

            feature_result=feature_result,

            growth_result=growth_result,

            latest_pattern=latest_pattern,

            recent_patterns=recent_patterns,

            pattern_average=pattern_average,

            pattern_trend=pattern_trend,

            pattern_count=pattern_count,

        )

        identity_result = self.identity_engine.analyze(
            evidence
        )

        perspective = await self.identity_repository.get_latest_feedback(user_id)
        hypothesis_status = identity_result.stage.upper()
        if perspective and perspective.agreement in {"PARTIAL", "DISAGREE", "UNSURE"}:
            hypothesis_status = "REVIEW_REQUIRED"
            identity_result.warnings.append("사용자 의견을 반영해 정체성 가설의 재확인이 필요합니다.")

        current = await self.identity_repository.get_current(
            user_id
        )

        latest = await self.identity_repository.get_latest_version(
            user_id
        )

        if current:

            current.is_current = False

        identity = Identity(

            user_id=user_id,

            identity_name=identity_result.identity_name,

            description=identity_result.description or "",

            confidence=identity_result.confidence,

            version = latest + 1,

            is_current=True,

            candidate_snapshot=identity_result.ranking[:3],

            hypothesis_status=hypothesis_status,

        )

        await self.identity_repository.create(
            identity
        )

        identity_result.metadata["identity_id"] = identity.identity_id

        # Keyword

        for keyword in identity_result.keywords:

            await self.identity_repository.create_keyword(

                identity.identity_id,

                keyword,

            )

        # Strength

        for index, strength in enumerate(

            identity_result.strengths,

            start=1,

        ):

            await self.identity_repository.create_strength(

                identity.identity_id,

                strength,

                index,

            )

        # Growth Point

        for index, point in enumerate(

            identity_result.growth_points,

            start=1,

        ):

            await self.identity_repository.create_growth_point(

                identity.identity_id,

                point,

                index,

            )

        await self.identity_repository.commit()

        return IdentityResponse(

            identity_name=identity.identity_name,

            description=identity.description or "",

            confidence=float(identity.confidence),

            creativity_score=identity_result.creativity_score,

            execution_score=identity_result.execution_score,

            uncertainty_score=identity_result.uncertainty_score,

            keywords=identity_result.keywords,

            strengths=identity_result.strengths,

            growth_points=identity_result.growth_points,

            identity_scores=identity_result.identity_scores,

            ranking=identity_result.ranking,

            primary_identity=identity_result.primary_identity,

            secondary_identity=identity_result.secondary_identity,

            score_gap=identity_result.score_gap,

            matched_rules=identity_result.matched_rules,

            evidence=identity_result.evidence,

            metadata=identity_result.metadata,

            warnings=identity_result.warnings,

            candidates=identity_result.ranking[:3],

            hypothesis_status=hypothesis_status,
            user_perspective=self._feedback_dict(perspective),

        )

    # ======================================================
    # Current Identity
    # ======================================================

    async def get_current_identity(
        self,
        user_id: int,
    ) -> IdentityResponse:

        identity = await self.identity_repository.get_current(
            user_id
        )

        if identity is None:

            return IdentityResponse(

                identity_name="",

                description="",

                confidence=0,

                creativity_score=0,

                execution_score=0,

                uncertainty_score=0,

                keywords=[],

                strengths=[],

                growth_points=[],

                identity_scores={},

                ranking=[],

                primary_identity="",

                secondary_identity="",

                score_gap=0.0,

                matched_rules=[],

                evidence={},

                metadata={},

                warnings=[],

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

        pattern_count = await self.pattern_repository.get_pattern_count(
            user_id
        )

        pattern_average = await self.pattern_repository.get_pattern_average(
            user_id
        )

        pattern_trend = await self.pattern_repository.get_pattern_trend(
            user_id
        )

        return IdentityResponse(

            identity_name=identity.identity_name,

            description=identity.description or "",

            confidence=float(identity.confidence),

            creativity_score=int(
                round(
                    pattern_average.get(
                        CREATIVITY,
                        0,
                    )
                )
            ),

            execution_score=int(
                round(
                    pattern_average.get(
                        EXECUTION,
                        0,
                    )
                )
            ),

            uncertainty_score=int(
                round(
                    pattern_average.get(
                        UNCERTAINTY,
                        0,
                    )
                )
            ),

            keywords=keywords,

            strengths=strengths,

            growth_points=growth_points,

            identity_scores={},

            ranking=[],

            primary_identity=identity.identity_name,

            secondary_identity="",

            score_gap=0.0,

            matched_rules=[],

            evidence={

                "source_layer": "Layer3",

                "pattern_count": pattern_count,

                "pattern_average": pattern_average,

                "pattern_trend": pattern_trend,

            },

            metadata={

                "identity_id": identity.identity_id,

                "version": identity.version,

                "generated_at": identity.generated_at,

                "is_current": identity.is_current,

            },

            warnings=[],

            candidates=self._candidate_snapshot(identity),

            hypothesis_status=identity.hypothesis_status,

            feedback=self._feedback_dict(await self.identity_repository.get_feedback(identity.identity_id, user_id)),

            user_perspective=self._feedback_dict(await self.identity_repository.get_latest_feedback(user_id)),

        )


    # ======================================================
    # Detail
    # ======================================================

    async def get_detail(
        self,
        identity_id: int,
        user_id: int,
    ) -> IdentityResponse:

        identity = await self.identity_repository.get_by_id(
            identity_id
        )

        if identity is None or identity.user_id != user_id:
            raise ValueError("Identity not found.")

        keywords = await self.identity_repository.get_keywords(
            identity.identity_id
        )

        strengths = await self.identity_repository.get_strengths(
            identity.identity_id
        )

        growth_points = await self.identity_repository.get_growth_points(
            identity.identity_id
        )

        pattern_average = await self.pattern_repository.get_pattern_average(
            identity.user_id
        )

        return IdentityResponse(

            identity_name=identity.identity_name,

            description=identity.description or "",

            confidence=float(
                identity.confidence
            ),

            creativity_score=int(
                round(pattern_average.get(CREATIVITY, 0))
            ),

            execution_score=int(
                round(pattern_average.get(EXECUTION, 0))
            ),

            uncertainty_score=int(
                round(pattern_average.get(UNCERTAINTY, 0))
            ),

            keywords=keywords,

            strengths=strengths,

            growth_points=growth_points,

            identity_scores={},

            ranking=[],

            primary_identity=identity.identity_name,

            secondary_identity="",

            score_gap=0.0,

            matched_rules=[],

            evidence={},

            metadata={

                "identity_id": identity.identity_id,

                "version": identity.version,

                "generated_at": identity.generated_at,

            },

            warnings=[],

            candidates=self._candidate_snapshot(identity),

            hypothesis_status=identity.hypothesis_status,

            feedback=self._feedback_dict(await self.identity_repository.get_feedback(identity.identity_id, user_id)),

            user_perspective=self._feedback_dict(await self.identity_repository.get_latest_feedback(user_id)),
        )

    async def submit_feedback(self, identity_id: int, user_id: int, request: IdentityFeedbackRequest):
        identity = await self.identity_repository.get_by_id(identity_id)
        if identity is None or identity.user_id != user_id:
            raise ValueError("Identity not found.")
        correction = request.correction_text.strip() if request.correction_text else None
        if request.agreement in {"PARTIAL", "DISAGREE"} and not correction:
            raise ValueError("A correction is required for partial agreement or disagreement.")
        feedback = await self.identity_repository.upsert_feedback(
            identity_id, user_id, request.agreement, correction
        )
        await self.identity_repository.commit()
        return IdentityFeedbackResponse(
            feedback_id=feedback.feedback_id,
            identity_id=feedback.identity_id,
            agreement=feedback.agreement,
            correction_text=feedback.correction_text,
            updated_at=feedback.updated_at,
        )

    @staticmethod
    def _feedback_dict(feedback):
        if feedback is None:
            return None
        return {
            "feedback_id": feedback.feedback_id,
            "identity_id": feedback.identity_id,
            "agreement": feedback.agreement,
            "correction_text": feedback.correction_text,
            "updated_at": feedback.updated_at,
            "provenance": feedback.provenance,
        }

    @staticmethod
    def _candidate_snapshot(identity):
        if identity.candidate_snapshot:
            return list(identity.candidate_snapshot)
        return [{
            "rank": 1,
            "identity_name": identity.identity_name,
            "score": None,
            "historical": True,
        }]

    # ======================================================
    # Identity History
    # ======================================================

    async def get_history(
        self,
        user_id: int,
    ) -> IdentityHistoryResponse:

        identities = await self.identity_repository.get_history(
            user_id
        )

        return IdentityHistoryResponse(

            histories=[

                IdentityHistoryItemResponse(

                    identity_id=identity.identity_id,

                    identity_name=identity.identity_name,

                    version=identity.version,

                    confidence=float(
                        identity.confidence
                    ),

                    generated_at=identity.generated_at,

                    is_current=identity.is_current,

                )

                for identity in identities

            ]

        )
