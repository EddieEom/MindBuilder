from app.features.auth.schemas import (
    UserProfileResponse,
    UpdateProfileImageResponse,
    UpdateNicknameResponse,
)

from app.repositories.growth_repository import GrowthRepository
from app.repositories.life_map_repository import LifeMapRepository
from app.repositories.pattern_repository import PatternRepository
from app.repositories.archive_repository import ArchiveRepository

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