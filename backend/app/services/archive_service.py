from app.ai.identity import identity_builder
from app.repositories.archive_repository import ArchiveRepository
from app.repositories.pattern_repository import PatternRepository
from app.repositories.identity_repository import IdentityRepository
from app.repositories.life_map_repository import LifeMapRepository
from app.repositories.growth_repository import GrowthRepository
from app.repositories.operating_system_repository import OperatingSystemRepository
from app.repositories.scan_repository import ScanRepository
from datetime import date

class ArchiveService:

    def __init__(
        self,
        archive_repository: ArchiveRepository = None,
        pattern_repository: PatternRepository = None,
        identity_repository: IdentityRepository = None,
        life_map_repository: LifeMapRepository = None,
        growth_repository: GrowthRepository = None,
        os_repository: OperatingSystemRepository = None,
        scan_repository: ScanRepository = None,
        db=None,
    ):
        if db is not None:
            self.archive_repository = archive_repository or ArchiveRepository(db)
            self.pattern_repository = pattern_repository or PatternRepository(db)
            self.identity_repository = identity_repository or IdentityRepository(db)
            self.life_map_repository = life_map_repository or LifeMapRepository(db)
            self.growth_repository = growth_repository or GrowthRepository(db)
            self.os_repository = os_repository or OperatingSystemRepository(db)
            self.scan_repository = scan_repository or ScanRepository(db)
        else:
            self.archive_repository = archive_repository
            self.pattern_repository = pattern_repository
            self.identity_repository = identity_repository
            self.life_map_repository = life_map_repository
            self.growth_repository = growth_repository
            self.os_repository = os_repository
            self.scan_repository = scan_repository

    async def record_onboarding_workflow(
        self,
        user_id: int,
        scan_id: int,
        response,
    ):
        """
        Onboarding Workflow 완료 후 타임라인 기록 순서 캡슐화 (단일 트랜잭션)
        """
        try:
            # 1. Scan 기록
            await self.record_scan(user_id=user_id, scan_id=scan_id)

            # 2. Pattern 기록
            pattern_id = getattr(response, "pattern_id", None)
            if pattern_id:
                await self.record_pattern(user_id=user_id, pattern_id=pattern_id)

            # 3. Growth 기록
            if hasattr(response, "growth") and response.growth and response.growth.metadata:
                growth_id = response.growth.metadata.get("growth_analysis_id")
                if growth_id:
                    await self.record_growth(user_id=user_id, growth_analysis_id=growth_id)

            # 4. Identity 기록
            if hasattr(response, "identity") and response.identity and response.identity.metadata:
                identity_id = response.identity.metadata.get("identity_id")
                if identity_id:
                    await self.record_identity(user_id=user_id, identity_id=identity_id)

            await self.archive_repository.commit()
        except Exception:
            await self.archive_repository.rollback()
            raise

    async def record_lifemap_workflow(
        self,
        user_id: int,
        life_map_id: int,
    ):
        """
        LifeMap Workflow 완료 후 타임라인 기록
        """
        try:
            await self.record_lifemap(user_id=user_id, life_map_id=life_map_id)
            await self.archive_repository.commit()
        except Exception:
            await self.archive_repository.rollback()
            raise

    async def record_operating_system_workflow(
        self,
        user_id: int,
        os_id: int,
    ):
        """
        OperatingSystem Workflow 완료 후 타임라인 기록
        """
        try:
            await self.record_operating_system(user_id=user_id, os_id=os_id)
            await self.archive_repository.commit()
        except Exception:
            await self.archive_repository.rollback()
            raise

    async def record_scan(
        self,
        user_id: int,
        scan_id: int,
    ):
        await self.archive_repository.create_event(
            user_id=user_id,
            event_type="SCAN_COMPLETED",
            reference_id=scan_id,
            title="Mind Scan",
            summary=self._build_scan_summary(),
        )

    async def record_pattern(
        self,
        user_id: int,
        pattern_id: int,
    ):
        pattern = await self.pattern_repository.get_by_id(pattern_id)
        
        summary = self._build_pattern_summary(pattern)

        await self.archive_repository.create_event(
            user_id=user_id,
            event_type="PATTERN_ANALYZED",
            reference_id=pattern_id,
            title="Pattern 분석 결과",
            summary=summary,
        )

    async def record_growth(
        self,
        user_id: int,
        growth_analysis_id: int,
    ):
        growth_analysis = await self.growth_repository.get_growth_analysis(
            growth_analysis_id
        )

        summary = None

        if growth_analysis:

            growth_items = await self.growth_repository.get_growth_items(
                growth_analysis.growth_analysis_id
            )

            summary = self._build_growth_summary(
                growth_items
            )

        await self.archive_repository.create_event(
            user_id=user_id,
            event_type="GROWTH_ANALYZED",
            reference_id=growth_analysis_id,
            title="Growth 분석 결과",
            summary=summary,
        )

    async def record_identity(
        self,
        user_id: int,
        identity_id: int,
    ):
        identity = await self.identity_repository.get_by_id(identity_id)
        title, summary = self._build_identity_summary(identity)

        await self.archive_repository.create_event(
            user_id=user_id,
            event_type="IDENTITY_CREATED",
            reference_id=identity_id,
            title=title,
            summary=summary,
        )

    async def record_lifemap(
        self,
        user_id: int,
        life_map_id: int,
    ):
        nodes = await self.life_map_repository.get_nodes(life_map_id)
        summary = self._build_lifemap_summary(nodes)

        await self.archive_repository.create_event(
            user_id=user_id,
            event_type="LIFEMAP_CREATED",
            reference_id=life_map_id,
            title="LifeMap 업데이트",
            summary=summary,
        )

    async def record_operating_system(
        self,
        user_id: int,
        os_id: int,
    ):
        os_data = await self.os_repository.get_by_id(os_id)
        summary = self._build_os_summary(os_data)

        await self.archive_repository.create_event(
            user_id=user_id,
            event_type="OS_UPDATED",
            reference_id=os_id,
            title="Human Operating System 업데이트",
            summary=summary,
        )


    # ==========================================================
    # Summary Builder
    # ==========================================================

    def _build_scan_summary(self) -> str:
        return "오늘의 사고 데이터 분석이 완료되었습니다."


    def _build_pattern_summary(self, pattern) -> str:

        if pattern is None:
            return "사고 패턴 분석 완료"

        scores = {
            "미래지향성": pattern.future_score,
            "창의성": pattern.creativity_score,
            "실행력": pattern.execution_score,
            "불확실성 대응": pattern.uncertainty_score,
            "완벽주의": pattern.perfectionism_score,
            "회복탄력성": pattern.resilience_score,
        }

        top_scores = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:2]

        return ", ".join(
            f"{name} {score:.0f}"
            for name, score in top_scores
        )


    def _build_growth_summary(
        self,
        growth_items,
    ) -> str | None:

        if not growth_items:
            return None

        return growth_items[0].title


    def _build_identity_summary(
        self,
        identity,
    ) -> tuple[str, str | None]:

        if identity is None:

            return (
                "Identity",
                None,
            )

        return (
            identity.identity_name,
            identity.description,
        )


    def _build_lifemap_summary(
        self,
        nodes,
    ) -> str | None:

        if not nodes:
            return None

        return ", ".join(
            node.title
            for node in nodes[:3]
        )


    def _build_os_summary(
        self,
        os_data,
    ) -> str:

        if (
            os_data is None
            or
            os_data.version is None
        ):
            return "새로운 운영체제 버전이 생성되었습니다."

        return f"버전 {os_data.version} 업데이트 완료"
                
 


    async def get_recent_archive(
        self,
        user_id: int,
        limit: int = 30,
    ):
        return await self.archive_repository.get_recent_events(user_id=user_id, limit=limit)

    async def get_archive_by_type(
        self,
        user_id: int,
        event_type: str,
        limit: int = 50,
    ):
        return await self.archive_repository.get_events_by_type(
            user_id=user_id,
            event_type=event_type,
            limit=limit,
        )

    async def get_archive_calendar(
        self,
        user_id: int,
        date: date,
    ):
        return await self.archive_repository.get_events_by_date(
            user_id=user_id,
            date=date,
        )

    async def get_growth_timeline(
        self,
        user_id: int,
        limit: int = 50,
    ):
        return await self.archive_repository.get_events_by_type(
            user_id=user_id,
            event_type="GROWTH_ANALYZED",
            limit=limit,
        )
