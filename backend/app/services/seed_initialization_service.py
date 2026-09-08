from dataclasses import asdict, dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.feature_extractor.constants import FEATURE_KEYS
from app.repositories.answer_repository import AnswerRepository
from app.repositories.archive_repository import ArchiveRepository
from app.repositories.data_confidence_repository import (
    DataConfidenceRepository,
)
from app.repositories.feature_repository import FeatureRepository
from app.repositories.life_map_repository import LifeMapRepository
from app.repositories.operating_system_repository import (
    OperatingSystemRepository,
)
from app.repositories.scan_repository import ScanRepository
from app.services.life_map_service import LifeMapService
from app.services.operating_system_service import OperatingSystemService


@dataclass(slots=True)
class SeedInitializationResult:
    seed_exists: bool
    created_now: bool
    stage: str
    data_confidence: float
    scan_count: int
    life_map_id: int | None
    os_id: int | None
    archive_event_id: int | None

    def to_dict(
        self,
    ) -> dict:
        return asdict(self)


class SeedInitializationService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.answer_repository = AnswerRepository(db)
        self.archive_repository = ArchiveRepository(db)
        self.data_confidence_repository = DataConfidenceRepository(db)
        self.feature_repository = FeatureRepository(db)
        self.life_map_repository = LifeMapRepository(db)
        self.operating_system_repository = OperatingSystemRepository(db)
        self.scan_repository = ScanRepository(db)

    async def initialize_seed(
        self,
        user_id: int,
        scan_id: int,
    ) -> SeedInitializationResult:
        scan_count = await self.scan_repository.count_completed_scans(
            user_id=user_id,
        )

        answer_question_count = (
            await self.answer_repository.count_distinct_questions_by_scan_id(
                scan_id
            )
        )

        other_input_count = (
            await self.answer_repository.count_details_by_scan_id(
                scan_id
            )
        )

        feature_count = await self.feature_repository.count_by_scan_id(
            scan_id
        )

        quality = await self.feature_repository.quality_metrics(
            scan_id=scan_id,
            user_id=user_id,
        )

        confidence_score = self._calculate_confidence_score(
            answer_question_count=answer_question_count,
            feature_count=feature_count,
            other_input_count=other_input_count,
            evidence_count=int(quality["evidence_count"]),
            evidence_strength=quality["evidence_strength"],
            conflict_strength=quality["conflict_strength"],
            longitudinal_stability=quality["stability"],
        )

        await self.data_confidence_repository.upsert(
            user_id=user_id,
            scan_count=scan_count,
            confidence_score=confidence_score,
            current_stage="Seed",
        )

        life_map = await self.life_map_repository.get_current(
            user_id
        )

        life_map_id = (
            life_map.life_map_id
            if life_map is not None
            else None
        )

        if life_map is None:
            life_map_response = await LifeMapService(
                self.db
            ).analyze(
                user_id=user_id
            )
            life_map_id = int(
                life_map_response.metadata["life_map_id"]
            )

        operating_system = await self.operating_system_repository.get_current(
            user_id
        )

        os_id = (
            operating_system.os_id
            if operating_system is not None
            else None
        )

        archive_event_id = None
        created_now = False


        os_response = await OperatingSystemService(
            self.db
        ).generate(
            user_id
        )

        os_id = os_response.os_id
        created_now = True

        archive_event = await self.archive_repository.create_event(
            user_id=user_id,
            event_type="SEED_CREATED",
            reference_id=os_id,
            title="초기 Seed 생성 완료",
            summary=(
                "첫 번째 사고 패턴 분석을 기반으로 "
                "Human OS 초기 상태가 생성되었습니다."
            ),
        )
        archive_event_id = archive_event.event_id

        await self.archive_repository.commit()

        return SeedInitializationResult(
            seed_exists=(
                life_map_id is not None
                and os_id is not None
            ),
            created_now=created_now,
            stage="Seed",
            data_confidence=confidence_score,
            scan_count=scan_count,
            life_map_id=life_map_id,
            os_id=os_id,
            archive_event_id=archive_event_id,
        )
    
    def _calculate_confidence_score(
        self,
        answer_question_count: int,
        feature_count: int,
        other_input_count: int,
        evidence_count: int,
        evidence_strength: float,
        conflict_strength: float,
        longitudinal_stability: float,
    ) -> float:
        total_seed_questions = 6
        answer_completeness = min(
            answer_question_count / total_seed_questions,
            1.0,
        )

        feature_coverage = min(
            feature_count / len(FEATURE_KEYS),
            1.0,
        )

        evidence_diversity = min(evidence_count / 8.0, 1.0)
        specificity = min(other_input_count / 2.0, 1.0)
        score = (
            answer_completeness * 20.0
            + feature_coverage * 15.0
            + evidence_strength * 20.0
            + evidence_diversity * 15.0
            + longitudinal_stability * 20.0
            + specificity * 10.0
            - conflict_strength * 15.0
        )

        return round(
            max(
                10.0,
                min(
                    score,
                    95.0,
                ),
            ),
            2,
        )
