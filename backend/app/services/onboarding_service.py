from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.question import (
    QuestionOptionResponse,
    QuestionResponse,
    QuestionSetResponse,
)

from app.schemas.answer import (
    SubmitAnswersRequest,
)

from app.schemas.pattern_analysis import PatternAnalysisResponse
from app.schemas.scan import StartOnboardingResponse

class OnboardingService:
    """
    Onboarding Service

    Repository에서 조회한 데이터를
    API Response 형태로 가공한다.
    """

    """
    Onboarding Service

    Repository에서 조회한 데이터를
    API Response 형태로 가공한다.
    """

    def __init__(
        self,
        question_repository,
        scan_repository,
        answer_repository=None,
        pattern_analysis_service=None,
    ):

        self.question_repository = question_repository
        self.scan_repository = scan_repository
        self.answer_repository = answer_repository
        self.pattern_analysis_service = pattern_analysis_service

    async def get_onboarding_questions(self) -> QuestionSetResponse:
        """
        Seed Onboarding 질문 조회

        활성화된 Question Set을 조회하고
        Flutter에서 사용할 Response 형태로 변환한다.
        """

        question_set = await self.question_repository.get_active_question_set()

        if question_set is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="해당 Scan에 접근할 권한이 없습니다.",
            )

        questions = []

        # QuestionSetItem의 display_order 기준으로 정렬
        sorted_items = sorted(
            question_set.question_set_items,
            key=lambda item: item.display_order,
        )

        for item in sorted_items:

            question = item.question

            options = sorted(
                question.options,
                key=lambda option: option.display_order,
            )

            option_responses = [
                QuestionOptionResponse(
                    option_id=option.option_id,
                    option_text=option.option_text,
                    option_value=option.option_value,
                    display_order=option.display_order,
                    is_other=option.is_other,
                )
                for option in options
            ]

            questions.append(
                QuestionResponse(
                    question_id=question.question_id,
                    question_code=question.question_code,
                    title=question.title,
                    description=question.description,
                    question_type=question.question_type,
                    display_order=question.display_order,
                    options=option_responses,
                )
            )

        return QuestionSetResponse(
            set_id=question_set.set_id,
            set_name=question_set.set_name,
            description=question_set.description,
            target_stage=question_set.target_stage,
            questions=questions,
        )
    

    async def start_onboarding(
        self,
        current_user: User,
    ) -> StartOnboardingResponse:

        scan = await self.scan_repository.get_in_progress_scan(
            user_id=current_user.user_id,
            scan_type="ONBOARDING",
        )

        if scan is None:
            scan = await self.scan_repository.create_scan(
                user_id=current_user.user_id,
                scan_type="ONBOARDING",
            )

        return StartOnboardingResponse(
            scan_id=scan.scan_id,
            status=scan.status,
            started_at=scan.started_at,
        )
    
    async def submit_answers(
        self,
        current_user: User,
        request: SubmitAnswersRequest,
    ) -> PatternAnalysisResponse:
        """
        온보딩 답변 저장

        - answers 저장
        - 기타 입력(answer_details) 저장
        - 마지막에 Commit
        """

        try:

            for answer in request.answers:

                saved_answer = await self.answer_repository.create_answer(
                    scan_id=request.scan_id,
                    question_id=answer.question_id,
                    option_id=answer.option_id,
                    point_value=answer.point_value,
                )

                # 기타 입력이 있는 경우
                if answer.detail_text:

                    await self.answer_repository.create_answer_detail(
                        answer_id=saved_answer.answer_id,
                        detail_text=answer.detail_text,
                    )

            scan = await self.scan_repository.get_by_id(request.scan_id)

            if scan is None:
                raise ValueError("존재하지 않는 Scan입니다.")

            if scan.status == "COMPLETED":
                raise ValueError("이미 완료된 Scan입니다.")
            
            if scan.user_id != current_user.user_id:
                raise PermissionError("해당 Scan에 접근할 권한이 없습니다.")

            for answer in request.answers:
                ...

            await self.scan_repository.update_completed_scan(scan)

            await self.answer_repository.commit()

            result = await self.pattern_analysis_service.analyze(
                scan.scan_id
            )

            return PatternAnalysisResponse(

                pattern_id=result.metadata["pattern_id"],

                confidence=result.confidence_score,

                scores=result.scores,

                patterns=result.patterns,

                metadata=result.metadata,
            )

        except Exception:

            await self.answer_repository.rollback()

            raise
