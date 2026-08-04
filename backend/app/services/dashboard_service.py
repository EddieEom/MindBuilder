from app.schemas.dashboard import (
    DashboardArchiveResponse,
    DashboardChangeItemResponse,
    DashboardHumanOSResponse,
    DashboardInsightResponse,
    DashboardNextActionResponse,
    DashboardResponse,
)


class DashboardService:

    def __init__(
        self,
        dashboard_repository,
    ):
        self.dashboard_repository = dashboard_repository

    async def get_dashboard(
        self,
        user_id: int,
    ) -> DashboardResponse:

        operating_system = await self.dashboard_repository.get_current_os(
            user_id
        )

        confidence = await self.dashboard_repository.get_data_confidence(
            user_id
        )

        insight = await self.dashboard_repository.get_latest_insight(
            user_id
        )

        next_action = await self.dashboard_repository.get_next_action(
            user_id
        )

        pattern = await self.dashboard_repository.get_latest_pattern(
            user_id
        )

        archives = await self.dashboard_repository.get_recent_archives(
            user_id=user_id,
            limit=5,
        )

        recent_changes = []

        if pattern:

            recent_changes.append(
                DashboardChangeItemResponse(
                    metric="실행력",
                    value=float(pattern.execution_score),
                    change=0,
                )
            )

            recent_changes.append(
                DashboardChangeItemResponse(
                    metric="미래지향성",
                    value=float(pattern.future_score),
                    change=0,
                )
            )

            recent_changes.append(
                DashboardChangeItemResponse(
                    metric="창의성",
                    value=float(pattern.creativity_score),
                    change=0,
                )
            )

            recent_changes.append(
                DashboardChangeItemResponse(
                    metric="완벽주의",
                    value=float(pattern.perfectionism_score),
                    change=0,
                )
            )

        return DashboardResponse(

            human_os=DashboardHumanOSResponse(

                stage=(
                    operating_system.stage
                    if operating_system
                    else ""
                ),

                confidence=(
                    confidence.confidence_score
                    if confidence
                    else 0.0
                ),

                version=(
                    operating_system.version
                    if operating_system
                    else ""
                ),
            ),

            insight=DashboardInsightResponse(

                title=(
                    insight.title
                    if insight
                    else ""
                ),

                content=(
                    insight.content
                    if insight
                    else ""
                ),
            ),

            next_action=DashboardNextActionResponse(

                title=(
                    next_action.title
                    if next_action
                    else ""
                ),

                action_type=(
                    next_action.action_type
                    if next_action
                    else None
                ),

                action_url=(
                    next_action.action_url
                    if next_action
                    else None
                ),
            ),

            recent_changes=recent_changes,

            recent_archives=[

                DashboardArchiveResponse(

                    event_type=event.event_type,

                    title=event.title,

                    summary=event.summary,

                    created_at=event.created_at,

                )

                for event in archives

            ],
        )