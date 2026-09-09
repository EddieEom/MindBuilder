from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.feature_extractor.option_rules import OPTION_RULES
from app.models.scan import Answer, FeatureValue, Scan
from app.repositories.identity_repository import IdentityRepository
from app.repositories.question_repository import QuestionRepository
from app.schemas.question import QuestionOptionResponse, QuestionResponse, QuestionSetResponse


class AdaptiveScanService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.questions = QuestionRepository(db)

    async def get_questions(self, user_id: int, limit: int = 3) -> QuestionSetResponse:
        question_set = await self.questions.get_active_question_set()
        if question_set is None:
            raise ValueError("Active question set not found.")

        scan_id = (await self.db.execute(
            select(Scan.scan_id).where(
                Scan.user_id == user_id, Scan.status == "COMPLETED"
            ).order_by(Scan.completed_at.desc()).limit(1)
        )).scalar_one_or_none()
        confidence = {}
        recent_questions = set()
        perspective = await IdentityRepository(self.db).get_latest_feedback(user_id)
        if scan_id is not None:
            recent_questions = set((await self.db.execute(
                select(Answer.question_id).where(Answer.scan_id == scan_id)
            )).scalars().all())
            rows = (await self.db.execute(
                select(FeatureValue).join(Scan, Scan.scan_id == FeatureValue.scan_id).where(
                    Scan.user_id == user_id,
                    Scan.status == "COMPLETED",
                    FeatureValue.confidence_score > 0,
                ).order_by(Scan.started_at.desc(), Scan.scan_id.desc())
            )).scalars().all()
            for row in rows:
                confidence.setdefault(row.feature_code, float(row.confidence_score))

        ranked = []
        for item in question_set.question_set_items:
            question = item.question
            if not question.is_active:
                continue
            features = sorted({
                rule["feature"]
                for option in OPTION_RULES.get(question.question_id, {}).values()
                for rule in option
                if rule.get("feature")
            })
            need = max((1.0 - confidence.get(code, 0.0) for code in features), default=0.25)
            # Prefer uncovered features while reducing immediate question repetition.
            priority = need - (0.2 if question.question_id in recent_questions else 0.0)
            ranked.append((priority, item.display_order, question, features))
        ranked.sort(key=lambda row: (-row[0], row[1]))

        responses = []
        for priority, _, question, features in ranked[:limit]:
            need = max((1.0 - confidence.get(code, 0.0) for code in features), default=0.25)
            prompts = [question.description or ""]
            if question.question_id in recent_questions:
                prompts.append("지난 답변과 비교해 지금도 같은지, 최근의 구체적인 경험을 떠올려 답해 주세요.")
            if perspective and perspective.agreement in {"PARTIAL", "DISAGREE", "UNSURE"}:
                prompts.append("이전 정체성 설명에 대한 의견을 다시 확인하고 있어요. 실제 경험에 가장 가까운 보기를 골라 주세요.")
                if perspective.correction_text:
                    prompts.append(f"내가 남긴 의견: {perspective.correction_text}")
            options = sorted(question.options, key=lambda option: option.display_order)
            responses.append(QuestionResponse(
                question_id=question.question_id,
                question_code=question.question_code,
                title=question.title,
                description="\n\n".join(part for part in prompts if part),
                question_type=question.question_type,
                display_order=question.display_order,
                options=[QuestionOptionResponse.model_validate(option) for option in options],
                target_features=features,
                information_need=round(need, 4),
                selection_reason=(
                    "아직 근거가 부족한 특성을 보강하기 위해 선택했습니다."
                    if features else "최근 응답의 일관성을 다시 확인하기 위해 선택했습니다."
                ),
            ))
        return QuestionSetResponse(
            set_id=question_set.set_id,
            set_name=f"{question_set.set_name} Adaptive",
            description="현재 데이터에서 정보가 부족한 영역을 우선 확인합니다.",
            target_stage=question_set.target_stage,
            questions=responses,
            adaptive=True,
            source_scan_id=scan_id,
        )
