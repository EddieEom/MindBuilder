from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.operating_system_repository import (
    OperatingSystemRepository,
)
from app.repositories.pattern_repository import PatternRepository
from app.repositories.identity_repository import IdentityRepository
from app.repositories.life_map_repository import LifeMapRepository
from app.repositories.growth_repository import GrowthRepository

from app.models.operating_system import (
    OperatingSystem,
)
from app.models.analysis import PatternAnalysis, DataConfidence
from app.models.identity import Identity
from app.models.lifemap import LifeMap
from app.models.growth import GrowthAnalysis
from app.schemas.operating_system import (
    OperatingSystemResponse,
    OSCoreValueResponse,
    OperatingSystemVersionResponse,
)

class OperatingSystemService:
    async def _visual_data(self, user_id: int) -> dict:
        confidence = await self._get_data_confidence(user_id)
        pattern = await self.pattern_repository.get_latest_pattern(user_id)
        return {
            "confidence_score": float(confidence.confidence_score) if confidence else None,
            "pattern_scores": {
                name: float(getattr(pattern, name + "_score"))
                for name in ("future", "creativity", "execution", "uncertainty", "perfectionism", "resilience")
            } if pattern else {},
        }

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.os_repository = OperatingSystemRepository(db)
        self.pattern_repository = PatternRepository(db)
        self.identity_repository = IdentityRepository(db)
        self.life_map_repository = LifeMapRepository(db)
        self.growth_repository = GrowthRepository(db)

    async def generate(
        self,
        user_id: int,
    ) -> OperatingSystemResponse:
        latest_pattern = await self.pattern_repository.get_latest_pattern(
            user_id=user_id
        )

        if latest_pattern is None:
            raise ValueError(
                "Latest Pattern not found. Operating System requires Layer2 Pattern data."
            )

        identity = await self.identity_repository.get_current(
            user_id
        )

        if identity is None:
            raise ValueError(
                "Current Identity not found. Operating System requires Layer3 Identity data."
            )

        life_map = await self.life_map_repository.get_current(
            user_id
        )

        if life_map is None:
            raise ValueError(
                "Current LifeMap not found. Operating System requires Layer4 LifeMap data."
            )

        growth_analysis = await self.growth_repository.get_by_pattern(
            latest_pattern.pattern_id
        )

        if growth_analysis is None:
            raise ValueError(
                "Current Growth not found. Operating System requires Growth data."
            )

        core_values = await self._build_core_values(
            latest_pattern,
            identity,
            life_map,
            growth_analysis,
        )

        operating_system = OperatingSystem(
            user_id=user_id,
            identity_id=identity.identity_id,
            life_map_id=life_map.life_map_id,
            version=self._build_version(latest_pattern, identity, life_map, growth_analysis),
            is_current=True,
        )

        await self.db.execute(
            text(
                "UPDATE operating_systems SET is_current = false WHERE user_id = :user_id AND is_current = true"
            ),
            {"user_id": user_id},
        )

        operating_system = await self.os_repository.create_operating_system(
            operating_system
        )

        for index, value in enumerate(core_values, start=1):
            core_value = await self.os_repository.get_or_create_core_value(
                value_name=value["value_name"] or "",
                description=value.get("description"),
            )
            await self.os_repository.create_os_core_value(
                operating_system_id=operating_system.os_id,
                value_id=core_value.value_id,
                priority=index,
            )

        await self.os_repository.commit()

        thinking_pattern = await self._derive_thinking_pattern(latest_pattern, identity, growth_analysis)
        decision_pattern = await self._derive_decision_pattern(latest_pattern, identity, growth_analysis)
        operating_rules = await self._derive_operating_rules(latest_pattern, identity, life_map, growth_analysis)

        stage = await self._derive_stage(operating_system)
        data_confidence = await self._derive_data_confidence(
            user_id=user_id,
            identity=identity,
        )

        response = await self._to_response(
            operating_system=operating_system,
            core_values=core_values,
            thinking_pattern=thinking_pattern,
            decision_pattern=decision_pattern,
            operating_rules=operating_rules,
            stage=stage,
            data_confidence=data_confidence,
        )

        return response

    async def get_current(
        self,
        user_id: int,
    ) -> OperatingSystemResponse:
        operating_system = await self.os_repository.get_current(user_id)

        if operating_system is None:
            raise ValueError("Current Operating System not found.")

        return await self._build_operating_system_response(
            operating_system
        )

    async def get_history(
        self,
        user_id: int,
    ) -> list[OperatingSystemResponse]:
        operating_systems = await self.os_repository.get_history(user_id)

        results = []
        for os_item in operating_systems:
            results.append(
                await self._build_operating_system_response(os_item)
            )

        return results

    async def _build_operating_system_response(
        self,
        operating_system: OperatingSystem,
    ) -> OperatingSystemResponse:
        core_values = [
            OSCoreValueResponse(
                value_name=value.core_value.value_name,
                description=value.core_value.description,
                priority=value.priority,
            )
            for value in operating_system.core_values
        ]

        latest_pattern = await self.pattern_repository.get_latest_pattern(
            operating_system.user_id
        )

        growth_analysis = None
        if latest_pattern is not None:
            growth_analysis = await self.growth_repository.get_by_pattern(
                latest_pattern.pattern_id
            )

        thinking_pattern = await self._derive_thinking_pattern(
            latest_pattern,
            operating_system.identity,
            growth_analysis,
        )

        decision_pattern = await self._derive_decision_pattern(
            latest_pattern,
            operating_system.identity,
            growth_analysis,
        )

        return OperatingSystemResponse(
            **await self._visual_data(operating_system.user_id),
            os_id=operating_system.os_id,
            version=operating_system.version,
            stage=await self._derive_stage(operating_system),
            data_confidence=await self._derive_data_confidence(
                operating_system.user_id,
                operating_system.identity,
            ),
            core_values=core_values,
            thinking_pattern=thinking_pattern,
            decision_pattern=decision_pattern,
            operating_rules=await self._derive_operating_rules(
                latest_pattern,
                operating_system.identity,
                operating_system.life_map,
                growth_analysis,
            ),
            metadata={
                "generated_at": operating_system.generated_at,
                "is_current": operating_system.is_current,
                "identity_id": operating_system.identity_id,
                "life_map_id": operating_system.life_map_id,
            },
        )

    async def _build_core_values(
        self,
        pattern: PatternAnalysis,
        identity: Identity,
        life_map: LifeMap,
        growth_analysis: GrowthAnalysis,
    ) -> list[dict[str, str | None]]:
        values: list[dict[str, str | None]] = []

        values.append(
            {
                "value_name": f"Pattern: {self._pattern_label(pattern)}",
                "description": self._pattern_description(pattern),
            }
        )

        values.append(
            {
                "value_name": f"Identity: {identity.identity_name}",
                "description": await self._identity_description(identity),
            }
        )

        values.append(
            {
                "value_name": f"LifeMap: {await self._life_map_focus(life_map)}",
                "description": "LifeMap에서 식별된 핵심 영역과 연결된 행동 지침입니다.",
            }
        )

        values.append(
            {
                "value_name": f"Growth: {await self._growth_focus(growth_analysis)}",
                "description": "Growth 분석에서 도출된 우선순위와 실행 제안입니다.",
            }
        )

        return values

    def _pattern_label(self, pattern: PatternAnalysis) -> str:
        scores = {
            "Execution": float(pattern.execution_score),
            "Creativity": float(pattern.creativity_score),
            "Future": float(pattern.future_score),
            "Uncertainty": float(pattern.uncertainty_score),
            "Perfectionism": float(pattern.perfectionism_score),
            "Resilience": float(pattern.resilience_score),
        }

        top_label = max(
            scores.items(),
            key=lambda item: item[1],
        )[0]

        return {
            "Execution": "Execution-led",
            "Creativity": "Creative",
            "Future": "Future-oriented",
            "Uncertainty": "Uncertainty-aware",
            "Perfectionism": "Quality-focused",
            "Resilience": "Resilient",
        }[top_label]

    def _pattern_description(self, pattern: PatternAnalysis) -> str:
        scores = {
            "Execution": float(pattern.execution_score),
            "Creativity": float(pattern.creativity_score),
            "Future": float(pattern.future_score),
            "Uncertainty": float(pattern.uncertainty_score),
            "Perfectionism": float(pattern.perfectionism_score),
            "Resilience": float(pattern.resilience_score),
        }

        sorted_scores = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        highest, highest_value = sorted_scores[0]
        second, second_value = sorted_scores[1]

        return (
            f"{highest}가 가장 높은 점수({highest_value:.0f})이며, "
            f"다음으로 {second}({second_value:.0f}) 수준을 보입니다."
        )

    async def _identity_description(self, identity: Identity) -> str:
        keywords = await self.identity_repository.get_keywords(identity.identity_id)
        strengths = await self.identity_repository.get_strengths(identity.identity_id)
        growth_points = await self.identity_repository.get_growth_points(identity.identity_id)

        identity_parts: list[str] = []

        if identity.description:
            identity_parts.append(identity.description)

        if keywords:
            identity_parts.append(f"핵심 키워드: {', '.join(keywords[:3])}")

        if strengths:
            identity_parts.append(f"강점: {', '.join(strengths[:2])}")

        if growth_points:
            identity_parts.append(f"성장 포인트: {', '.join(growth_points[:2])}")

        if not identity_parts:
            return "정체성 정보를 기반으로 한 핵심 가치입니다."

        return " ".join(identity_parts)

    async def _life_map_focus(self, life_map: LifeMap) -> str:
        nodes = await self.life_map_repository.get_nodes(life_map.life_map_id)

        if not nodes:
            return f"LifeMap v{life_map.version}"

        top_node = max(nodes, key=lambda node: float(node.importance or 0))
        node_type_name = top_node.node_type.name if top_node.node_type is not None else "핵심 영역"

        return f"{top_node.title} ({node_type_name})"

    async def _growth_focus(self, growth_analysis: GrowthAnalysis) -> str:
        growth_items = await self.growth_repository.get_growth_items(
            growth_analysis.growth_analysis_id
        )

        if not growth_items:
            return f"Growth v{growth_analysis.analysis_version}"

        top_item = min(growth_items, key=lambda item: item.priority or 0)

        return f"{top_item.title}"

    def _build_version(
        self,
        pattern: PatternAnalysis,
        identity: Identity,
        life_map: LifeMap,
        growth_analysis: GrowthAnalysis,
    ) -> str:
        return f"OS-{pattern.pattern_id}.{identity.version}.{life_map.version}.{growth_analysis.analysis_version}"

    async def _get_data_confidence(
        self,
        user_id: int,
    ) -> DataConfidence | None:
        stmt = select(DataConfidence).where(DataConfidence.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    def _confidence_label(self, score: float) -> str:
        value = float(score)

        if value >= 75:
            return "High"
        if value >= 40:
            return "Medium"
        return "Low"

    async def _derive_stage(
        self,
        operating_system: OperatingSystem,
    ) -> str:
        data_confidence = await self._get_data_confidence(
            operating_system.user_id
        )

        if data_confidence is not None:
            return data_confidence.current_stage

        latest_pattern = await self.pattern_repository.get_latest_pattern(
            operating_system.user_id
        )

        if latest_pattern is None:
            return "Seed"

        growth_analysis = await self.growth_repository.get_by_pattern(
            latest_pattern.pattern_id
        )

        if growth_analysis is not None and float(growth_analysis.confidence) >= 60:
            return "Growth"

        if float(latest_pattern.creativity_score) >= 55:
            return "Transition"

        return "Seed"

    async def _derive_data_confidence(
        self,
        user_id: int,
        identity: Identity,
    ) -> str:
        data_confidence = await self._get_data_confidence(user_id)

        if data_confidence is not None:
            return self._confidence_label(data_confidence.confidence_score)

        return self._confidence_label(identity.confidence)

    async def _derive_thinking_pattern(
        self,
        pattern: PatternAnalysis | None,
        identity: Identity,
        growth_analysis: GrowthAnalysis | None,
    ) -> str:
        if pattern is None:
            return "Identity-led" if float(identity.confidence) >= 50 else "Adaptive"

        scores = {
            "Execution-led": float(pattern.execution_score),
            "Creative-led": float(pattern.creativity_score),
            "Future-oriented": float(pattern.future_score),
            "Uncertainty-aware": float(pattern.uncertainty_score),
            "Quality-focused": float(pattern.perfectionism_score),
            "Resilient": float(pattern.resilience_score),
        }

        return max(
            scores.items(),
            key=lambda item: item[1],
        )[0]

    async def _derive_decision_pattern(
        self,
        pattern: PatternAnalysis | None,
        identity: Identity,
        growth_analysis: GrowthAnalysis | None,
    ) -> str:
        if pattern is None:
            return "Future-first" if float(identity.confidence) >= 50 else "Action-first"

        execution = float(pattern.execution_score)
        future = float(pattern.future_score)

        if future >= execution + 10:
            return "Future-first"

        if execution >= future + 10:
            return "Action-first"

        return "Balanced"

    async def _derive_operating_rules(
        self,
        pattern: PatternAnalysis | None,
        identity: Identity,
        life_map: LifeMap,
        growth_analysis: GrowthAnalysis | None,
    ) -> list[str]:
        rules: list[str] = []

        if float(identity.confidence) < 30:
            rules.append("정체성 신뢰도를 높이기 위해 핵심 강점을 재확인합니다.")

        if pattern is not None:
            if float(pattern.execution_score) >= float(pattern.creativity_score):
                rules.append(
                    "실행 중심의 작은 실천을 우선하여 빠른 피드백을 확보합니다."
                )
            else:
                rules.append("창의적 아이디어를 시도하며 새로운 방향을 검증합니다.")

            if float(pattern.future_score) >= float(pattern.execution_score):
                rules.append("미래 지향적 목표를 기준으로 의사결정을 세웁니다.")
            else:
                rules.append("현재 행동과 결과를 우선하여 빠르게 반복합니다.")
        else:
            rules.append(
                f"정체성 `{identity.identity_name}`에 맞춘 기준으로 의사결정을 설계합니다."
            )

        life_map_focus = await self._life_map_focus(life_map)
        rules.append(
            f"LifeMap 핵심 영역 '{life_map_focus}'에 리소스를 집중합니다."
        )

        if growth_analysis is not None:
            if float(growth_analysis.confidence) >= 50:
                rules.append("Growth 분석을 우선 고려하여 계획을 조정합니다.")
            else:
                rules.append(
                    "Growth 인사이트를 보완하며 추가 검증 데이터를 확보합니다."
                )

        return rules

    async def _to_response(
        self,
        operating_system: OperatingSystem,
        core_values: list[dict[str, str | None]],
        thinking_pattern: str,
        decision_pattern: str,
        operating_rules: list[str],
        stage: str,
        data_confidence: str,
    ) -> OperatingSystemResponse:
        return OperatingSystemResponse(
            **await self._visual_data(operating_system.user_id),
            os_id=operating_system.os_id,
            version=operating_system.version,
            stage=stage,
            data_confidence=data_confidence,
            core_values=[
                OSCoreValueResponse(
                    value_name=value["value_name"] or "",
                    description=value.get("description"),
                    priority=index,
                )
                for index, value in enumerate(core_values, start=1)
            ],
            thinking_pattern=thinking_pattern,
            decision_pattern=decision_pattern,
            operating_rules=operating_rules,
            metadata={
                "generated_at": operating_system.generated_at,
                "is_current": operating_system.is_current,
                "identity_id": operating_system.identity_id,
                "life_map_id": operating_system.life_map_id,
            },
        )

    # ======================================================
    # Version
    # ======================================================

    async def get_versions(
        self,
        user_id: int,
    ) -> list[OperatingSystemVersionResponse]:

        operating_systems = await self.os_repository.get_history(
            user_id
        )

        return [

            OperatingSystemVersionResponse(

                os_id=os.os_id,

                version=os.version,

                stage=os.stage,

                generated_at=os.generated_at,

                is_current=os.is_current,

            )

            for os in operating_systems

        ]

