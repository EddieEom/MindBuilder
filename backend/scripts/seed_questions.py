# backend/scripts/seed_questions.py

"""
Initial Seed Script

Purpose:
- Create default onboarding question set
- Insert Q1 ~ Q6
- Insert all question options
- Link QuestionSet <-> Questions

Run:
python -m backend.scripts.seed_questions
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app.core.database import AsyncSessionLocal

from app.models.question import (
    Question,
    QuestionOption,
    QuestionSet,
    QuestionSetItem,
)


QUESTIONS = [

    # ==========================================================
    # Q1
    # ==========================================================

    {
        "question_code": "Q1",
        "title": "지금 당신의 에너지는 어디에 가장 많이 사용되고 있나요?",
        "description": (
            "100포인트를 자유롭게 분배해주세요.\n"
            "최근 당신의 에너지가 가장 많이 사용되는 영역입니다."
        ),
        "question_type": "POINT",
        "display_order": 1,
        "options": [
            {
                "text": "프로젝트/일",
                "value": "energy_project",
            },
            {
                "text": "학습/공부",
                "value": "energy_study",
            },
            {
                "text": "운동/건강",
                "value": "energy_exercise",
            },
            {
                "text": "창작/아이디어",
                "value": "energy_creativity",
            },
            {
                "text": "인간관계",
                "value": "energy_relationship",
            },
            {
                "text": "휴식/여가",
                "value": "energy_rest",
            },
            {
                "text": "기타 (직접 입력)",
                "value": "energy_other",
                "is_other": True,
            },
        ],
    },

    # ==========================================================
    # Q2
    # ==========================================================

    {
        "question_code": "Q2",
        "title": "최근 당신을 가장 자주 고민하게 만드는 것은 무엇인가요?",
        "description": "최대 2개 선택",
        "question_type": "MULTI",
        "display_order": 2,
        "options": [
            {
                "text": "무엇부터 해야 할지 모르겠다.",
                "value": "direction_confusion",
            },
            {
                "text": "해야 할 일이 너무 많다.",
                "value": "overloaded",
            },
            {
                "text": "미래에 대한 생각이 자주 난다.",
                "value": "future_concern",
            },
            {
                "text": "잘하고 있는지 의심하게 된다.",
                "value": "self_doubt",
            },
            {
                "text": "다른 사람과 비교하게 된다.",
                "value": "comparison",
            },
            {
                "text": "쉬어야 하는데 쉬지 못한다.",
                "value": "cannot_rest",
            },
            {
                "text": "새로운 아이디어가 계속 떠오른다.",
                "value": "idea_overflow",
            },
            {
                "text": "특별히 없다.",
                "value": "none",
            },
            {
                "text": "기타 (직접 입력)",
                "value": "other",
                "is_other": True,
            },
        ],
    },

        # ==========================================================
    # Q3
    # ==========================================================

    {
        "question_code": "Q3",
        "title": "최근 당신의 행동 속도를 가장 느리게 만드는 것은 무엇인가요?",
        "description": "최대 2개 선택",
        "question_type": "MULTI",
        "display_order": 3,
        "options": [
            {
                "text": "생각이 너무 많다.",
                "value": "overthinking",
            },
            {
                "text": "무엇부터 해야 할지 모르겠다.",
                "value": "direction_confusion",
            },
            {
                "text": "시간이 부족하다.",
                "value": "lack_of_time",
            },
            {
                "text": "에너지가 부족하다.",
                "value": "low_energy",
            },
            {
                "text": "불안하다.",
                "value": "anxiety",
            },
            {
                "text": "완벽하게 하고 싶다.",
                "value": "perfectionism",
            },
            {
                "text": "집중력이 자주 끊긴다.",
                "value": "low_focus",
            },
            {
                "text": "계획이 없다.",
                "value": "no_plan",
            },
            {
                "text": "특별히 없다.",
                "value": "none",
            },
            {
                "text": "기타 (직접 입력)",
                "value": "other",
                "is_other": True,
            },
        ],
    },

    # ==========================================================
    # Q4
    # ==========================================================

    {
        "question_code": "Q4",
        "title": "지금 당신이 가장 얻고 싶은 상태는 무엇인가요?",
        "description": "1개 선택",
        "question_type": "SINGLE",
        "display_order": 4,
        "options": [
            {
                "text": "명확한 방향",
                "value": "want_direction",
            },
            {
                "text": "마음의 안정감",
                "value": "want_peace",
            },
            {
                "text": "성취감",
                "value": "want_achievement",
            },
            {
                "text": "성장감",
                "value": "want_growth",
            },
            {
                "text": "휴식",
                "value": "want_rest",
            },
            {
                "text": "자유",
                "value": "want_freedom",
            },
            {
                "text": "자신감",
                "value": "want_confidence",
            },
            {
                "text": "기타 (직접 입력)",
                "value": "other",
                "is_other": True,
            },
        ],
    },

        # ==========================================================
    # Q5
    # ==========================================================

    {
        "question_code": "Q5",
        "title": "최근 당신이 실제로 시간을 사용한 것은 무엇인가요?",
        "description": "다중 선택",
        "question_type": "MULTI",
        "display_order": 5,
        "options": [
            {
                "text": "프로젝트",
                "value": "actual_project",
            },
            {
                "text": "공부",
                "value": "actual_study",
            },
            {
                "text": "운동",
                "value": "actual_exercise",
            },
            {
                "text": "창작",
                "value": "actual_creativity",
            },
            {
                "text": "정리",
                "value": "actual_organization",
            },
            {
                "text": "휴식",
                "value": "actual_rest",
            },
            {
                "text": "인간관계",
                "value": "actual_relationship",
            },
            {
                "text": "기타 (직접 입력)",
                "value": "other",
                "is_other": True,
            },
        ],
    },

    # ==========================================================
    # Q6
    # ==========================================================

    {
        "question_code": "Q6",
        "title": "최근 당신의 긴장을 가장 크게 만드는 것은 무엇인가요?",
        "description": "1개 선택",
        "question_type": "SINGLE",
        "display_order": 6,
        "options": [
            {
                "text": "커리어",
                "value": "stress_career",
            },
            {
                "text": "미래",
                "value": "stress_future",
            },
            {
                "text": "돈",
                "value": "stress_money",
            },
            {
                "text": "프로젝트",
                "value": "stress_project",
            },
            {
                "text": "인간관계",
                "value": "stress_relationship",
            },
            {
                "text": "건강",
                "value": "stress_health",
            },
            {
                "text": "학업",
                "value": "stress_study",
            },
            {
                "text": "없음",
                "value": "stress_none",
            },
            {
                "text": "기타 (직접 입력)",
                "value": "other",
                "is_other": True,
            },
        ],
    },



]


async def insert_questions(db: AsyncSession):
    # 이미 Seed 질문 세트가 존재하면 종료
    result = await db.execute(
        select(QuestionSet).where(
            QuestionSet.set_name == "Seed Onboarding"
        )
    )

    existing_set = result.scalar_one_or_none()

    if existing_set:
        print("Seed questions already exist.")
        return

    # Question Set 생성
    question_set = QuestionSet(
        set_name="Seed Onboarding",
        description="초기 사용자 사고 데이터 수집 질문",
        target_stage="SEED",
        is_active=True,
    )

    db.add(question_set)
    await db.flush()

    # 질문 저장
    for question_data in QUESTIONS:
        question = Question(
            question_code=question_data["question_code"],
            title=question_data["title"],
            description=question_data.get("description"),
            question_type=question_data["question_type"],
            display_order=question_data["display_order"],
            is_active=True,
        )

        db.add(question)
        await db.flush()

        # 보기 저장
        for idx, option in enumerate(question_data["options"], start=1):
            question_option = QuestionOption(
                question_id=question.question_id,
                option_text=option["text"],
                option_value=option.get("value"),
                display_order=idx,
                is_other=option.get("is_other", False),
            )

            db.add(question_option)

        # QuestionSet 연결
        question_set_item = QuestionSetItem(
            set_id=question_set.set_id,
            question_id=question.question_id,
            display_order=question.display_order,
        )

        db.add(question_set_item)

    await db.flush()
    await db.commit()

    print("Seed onboarding questions inserted successfully.")




async def main():
    async with AsyncSessionLocal() as db:
        try:
            await insert_questions(db)

        except Exception as e:
            await db.rollback()
            print(f"Error: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(main())