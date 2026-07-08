from sqlalchemy.ext.asyncio import AsyncSession
from app.models.scan import Answer, AnswerDetail
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class AnswerRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_answer(
        self,
        scan_id: int,
        question_id: int,
        option_id: int,
        point_value: int | None = None,
    ) -> Answer:
        """
        답변 저장
        """

        answer = Answer(
            scan_id=scan_id,
            question_id=question_id,
            option_id=option_id,
            point_value=point_value or 0,
        )

        self.db.add(answer)

        # answer_id 생성
        await self.db.flush()
        await self.db.refresh(answer)

        return answer

    async def create_answer_detail(
        self,
        answer_id: int,
        detail_text: str,
    ) -> AnswerDetail:
        """
        기타 입력 저장
        """

        detail = AnswerDetail(
            answer_id=answer_id,
            detail_text=detail_text,
        )

        self.db.add(detail)

        await self.db.flush()
        await self.db.refresh(detail)

        return detail

    async def commit(self):
        """
        트랜잭션 Commit
        """
        await self.db.commit()

    async def rollback(self):
        """
        트랜잭션 Rollback
        """
        await self.db.rollback()

    # ======================================================
    # Scan의 모든 답변 조회
    # ======================================================

    async def get_answers_by_scan_id(
        self,
        scan_id: int,
    ) -> list[Answer]:
        """
        Scan의 모든 답변 조회
        (Feature Extraction용)
        """

        stmt = (
            select(Answer)
            .where(
                Answer.scan_id == scan_id
            )
            .options(
                selectinload(Answer.option),
                selectinload(Answer.detail),
            )
            .order_by(
                Answer.question_id.asc()
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()

    # ======================================================
    # Question 하나 조회
    # ======================================================

    async def get_answer(
        self,
        scan_id: int,
        question_id: int,
    ) -> Answer | None:

        stmt = (
            select(Answer)
            .where(
                Answer.scan_id == scan_id,
                Answer.question_id == question_id,
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()
    

    # PatternAnalysisService에서 답변이 존재하는가? 를 확인하는 함수
    async def exists_by_scan_id(
        self,
        scan_id: int,
    ) -> bool:

        stmt = (
            select(Answer.answer_id)
            .where(
                Answer.scan_id == scan_id
            )
            .limit(1)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none() is not None