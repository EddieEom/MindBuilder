class RecommendationService:

    def __init__(

        self,

        engine,

        repository,

    ):

        self.engine = engine
        self.repository = repository

    async def run(

        self,

        user_id,

        pattern,

        growth,

        identity,

        life_map,

        pattern_id,

    ):

        result = await self.engine.run(

            pattern,

            growth,

            identity,

            life_map,

        )

        await self.repository.save(

            user_id=user_id,

            pattern_id=pattern_id,

            result=result,

        )

        return result