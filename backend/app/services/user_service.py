from app.features.auth.schemas import (
    UserProfileResponse,
    UpdateProfileImageResponse,
    UpdateNicknameResponse,
)

from app.repositories.growth_repository import GrowthRepository
from app.repositories.life_map_repository import LifeMapRepository
from app.repositories.pattern_repository import PatternRepository
from app.repositories.archive_repository import ArchiveRepository
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

class UserService:

    def __init__(
        self,
        user_repository,
        identity_repository,
        operating_system_repository,
        growth_repository,
        life_map_repository,
        pattern_repository,
        archive_repository,
    ):

        self.user_repository = user_repository

        self.identity_repository = identity_repository

        self.operating_system_repository = operating_system_repository

        self.growth_repository = growth_repository

        self.life_map_repository = life_map_repository

        self.pattern_repository = pattern_repository

        self.archive_repository = archive_repository
    

    async def get_me(
        self,
        user_id: int,
    ) -> UserProfileResponse:

        user = await self.user_repository.get_by_id(
            user_id
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        provider = await self.user_repository.get_provider(
            user_id
        )

        identity = (
            await self.identity_repository.get_current(
                user_id
            )
        )

        operating_system = (
            await self.operating_system_repository.get_current(
                user_id
            )
        )

        scan_count = (
            await self.user_repository.get_scan_count(
                user_id
            )
        )

        pattern_count = (
            await self.user_repository.get_pattern_count(
                user_id
            )
        )

        analysis_count = (
            await self.user_repository.get_analysis_count(
                user_id
            )
        )

        archive_count = (
            await self.user_repository.get_archive_count(
                user_id
            )
        )

        goal_count = (
            await self.user_repository.get_goal_count(
                user_id
            )
        )

        return UserProfileResponse(

            nickname=user.nickname,

            profile_image=user.profile_image,

            identity_name=(
                identity.identity_name
                if identity
                else ""
            ),

            stage=(
                operating_system.stage
                if operating_system
                else ""
            ),

            scan_count=scan_count,
            pattern_count=pattern_count,
            analysis_count=analysis_count,
            archive_count=archive_count,
            goal_count=goal_count,
            email=user.email,
            provider=provider or "",
        )


    async def update_nickname(
        self,
        user_id: int,
        nickname: str,
    ) -> UpdateNicknameResponse:

        user = await self.user_repository.update_nickname(
            user_id=user_id,
            nickname=nickname,
        )

        await self.user_repository.commit()

        return UpdateNicknameResponse(

            nickname=user.nickname
        )


    async def update_profile_image(
        self,
        user_id: int,
        profile_image: str,
    ) -> UpdateProfileImageResponse:

        user = await self.user_repository.update_profile_image(
            user_id=user_id,
            profile_image=profile_image,
        )

        await self.user_repository.commit()

        return UpdateProfileImageResponse(

            profile_image=user.profile_image,
        )

    
    async def export_data(
        self,
        user_id: int,
    ) -> dict:

        user = await self.user_repository.get_by_id(
            user_id
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        identity = await self.identity_repository.get_current(
            user_id
        )

        growth = await self.growth_repository.get_current_growth(
            user_id
        )

        life_map = await self.life_map_repository.get_current(
            user_id
        )

        nodes = []

        if life_map:

            nodes = await self.life_map_repository.get_nodes(
                life_map.life_map_id
            )

        operating_system = (
            await self.operating_system_repository.get_current(
                user_id
            )
        )

        pattern = (
            await self.pattern_repository.get_latest_pattern(
                user_id
            )
        )

        archives = (
            await self.archive_repository.get_recent_events(
                user_id=user_id,
                limit=20,
            )
        )

        report = {

            "user": {

                "nickname": user.nickname,

                "email": user.email,

            },

            "identity": {

                "identity_name":
                    identity.identity_name if identity else "",

                "description":
                    identity.description if identity else "",

                "confidence":
                    identity.confidence if identity else 0,

            },

            "growth": {

                "growth_items": [
                    {
                        "title": item.title,
                        "description": item.content,
                    }

                    for item in (
                        growth.growth_items
                        if growth
                        else []
                    )
                ],

            },

            "lifemap": {
                "nodes": [
                    {
                        "title": node.title,
                        "node_type": node.node_type.code,
                    }
                    for node in nodes
                ],
            },

            "operating_system": {

                "version":
                    operating_system.version if operating_system else "",

                "stage":
                    operating_system.stage if operating_system else "",

            },

            "pattern": {

                "future_score":
                    pattern.future_score if pattern else 0,

                "creativity_score":
                    pattern.creativity_score if pattern else 0,

                "execution_score":
                    pattern.execution_score if pattern else 0,

                "resilience_score":
                    pattern.resilience_score if pattern else 0,

            },

            "archives": [

                {

                    "created_at": archive.created_at,

                    "archive_type": archive.event_type,

                }

                for archive in archives

            ],

        }
        return report

    async def export_pdf(self, user_id: int) -> bytes:
        report = await self.export_data(user_id)
        buffer = BytesIO()
        font_name = "HYSMyeongJo-Medium"
        try:
            pdfmetrics.getFont(font_name)
        except KeyError:
            pdfmetrics.registerFont(UnicodeCIDFont(font_name))
        document = canvas.Canvas(buffer)
        document.setTitle("MindBuilder Data Report")
        width, height = document._pagesize
        y = height - 48

        def line(text: str, size: int = 10, gap: int = 17) -> None:
            nonlocal y
            if y < 48:
                document.showPage()
                y = height - 48
            document.setFont(font_name, size)
            document.drawString(48, y, text[:95])
            y -= gap

        line("MindBuilder 사용자 데이터 보고서", 18, 30)
        line(f"사용자: {report['user']['nickname']} ({report['user']['email']})", 11, 25)
        line("Identity", 14, 22)
        line(f"이름: {report['identity']['identity_name']}")
        line(f"설명: {report['identity']['description']}")
        line(f"신뢰도: {report['identity']['confidence']}%", gap=25)
        line("Growth", 14, 22)
        for item in report["growth"]["growth_items"]:
            line(f"- {item['title']}: {item['description']}")
        y -= 8
        line("Life Map", 14, 22)
        for node in report["lifemap"]["nodes"]:
            line(f"- {node['title']} ({node['node_type']})")
        y -= 8
        line("Human OS", 14, 22)
        line(f"버전: {report['operating_system']['version']}")
        line(f"단계: {report['operating_system']['stage']}")
        document.save()
        return buffer.getvalue()

    async def delete_account(
        self,
        user_id: int,
    ):

        deleted = await self.user_repository.delete(
            user_id
        )

        if not deleted:
            raise ValueError(
                "User not found."
            )

        await self.user_repository.commit()

        return {
            "message": "회원탈퇴가 완료되었습니다."
        }
