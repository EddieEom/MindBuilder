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

        recent_patterns = await self.dashboard_repository.get_recent_patterns(
            user_id
        )

        pattern = recent_patterns[0] if recent_patterns else None
        previous_pattern = recent_patterns[1] if len(recent_patterns) > 1 else None

        archives = await self.dashboard_repository.get_recent_archives(
            user_id=user_id,
            limit=5,
        )

        recent_changes = []

        if pattern:
            def score_change(
                field: str,
            ) -> float | None:
                if previous_pattern is None:
                    return None

                return round(
                    float(getattr(pattern, field))
                    -
                    float(getattr(previous_pattern, field)),
                    2,
                )

            recent_changes.append(
                DashboardChangeItemResponse(
                    metric="실행력",
                    value=float(pattern.execution_score),
                    change=score_change("execution_score"),
                )
            )

            recent_changes.append(
                DashboardChangeItemResponse(
                    metric="미래지향성",
                    value=float(pattern.future_score),
                    change=score_change("future_score"),
                )
            )

            recent_changes.append(
                DashboardChangeItemResponse(
                    metric="창의성",
                    value=float(pattern.creativity_score),
                    change=score_change("creativity_score"),
                )
            )

            recent_changes.append(
                DashboardChangeItemResponse(
                    metric="완벽주의",
                    value=float(pattern.perfectionism_score),
                    change=score_change("perfectionism_score"),
                )
            )

        return DashboardResponse(

            human_os=(
                DashboardHumanOSResponse(
                    stage=operating_system.stage,
                    confidence=(
                        float(confidence.confidence_score)
                        if confidence
                        else None
                    ),
                    version=operating_system.version,
                )
                if operating_system
                else None
            ),

            insight=(
                DashboardInsightResponse(
                    title=insight.title,
                    content=insight.content,
                )
                if insight
                else None
            ),

            next_action=(
                DashboardNextActionResponse(
                    title=next_action.title,
                )
                if next_action
                else None
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
