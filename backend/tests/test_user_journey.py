"""Authenticated user journey contract using the real database with rollback."""
import unittest

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import engine, get_db
from app.main import app
from app.models.analysis import PatternAnalysis
from app.models.growth import GrowthAnalysis
from app.models.scan import Scan
from app.models.user import OAuthAccount, User


class UserJourneyTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        engine.echo = False
        self.connection = await engine.connect()
        self.transaction = await self.connection.begin()
        self.session = AsyncSession(
            bind=self.connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        stmt = (
            select(OAuthAccount, User)
            .join(User, User.user_id == OAuthAccount.user_id)
            .join(Scan, Scan.user_id == User.user_id)
            .join(PatternAnalysis, PatternAnalysis.scan_id == Scan.scan_id)
            .join(GrowthAnalysis, GrowthAnalysis.pattern_id == PatternAnalysis.pattern_id)
            .order_by(GrowthAnalysis.created_at.desc())
            .limit(1)
        )
        row = (await self.session.execute(stmt)).first()
        if row is None:
            await self.session.close()
            await self.transaction.rollback()
            await self.connection.close()
            await engine.dispose()
            self.skipTest("No OAuth user with completed analysis is available")
        self.oauth, self.user = row

        async def database():
            yield self.session

        app.dependency_overrides[get_db] = database
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://journey"
        )

    async def asyncTearDown(self):
        app.dependency_overrides.clear()
        await self.client.aclose()
        await self.session.close()
        await self.transaction.rollback()
        await self.connection.close()
        await engine.dispose()

    async def test_returning_user_reaches_every_end_content(self):
        login = await self.client.post(
            "/auth/login/oauth",
            json={
                "email": self.oauth.provider_email,
                "nickname": self.user.nickname,
                "provider": self.oauth.provider,
                "provider_user_id": self.oauth.provider_user_id,
                "profile_image": self.user.profile_image,
            },
        )
        self.assertEqual(login.status_code, 200)
        self.assertFalse(login.json()["is_new_user"])
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        questions = await self.client.get("/api/v1/onboarding/questions")
        self.assertEqual(questions.status_code, 200)
        self.assertGreater(len(questions.json()["questions"]), 0)
        start = await self.client.post("/api/v1/onboarding/start", headers=headers)
        self.assertEqual(start.status_code, 200)
        self.assertEqual(start.json()["status"], "IN_PROGRESS")

        checks = {
            "/auth/me": ("email", "scan_count"),
            "/api/v1/dashboard": ("human_os", "next_action"),
            "/api/v1/growth/current": ("metadata", "items"),
            "/api/v1/lifemap": ("nodes", "metadata"),
            "/api/v1/identity/current": ("identity_name", "metadata"),
            "/api/v1/operating-system/current": ("version", "pattern_scores"),
            "/api/v1/archive/recent": ("events",),
            "/api/v1/archive/summary": (),
            "/settings": ("notifications_enabled", "reminder_hour"),
            "/auth/export": ("user", "growth", "lifemap"),
        }
        for path, keys in checks.items():
            response = await self.client.get(path, headers=headers)
            self.assertEqual(response.status_code, 200, path)
            body = response.json()
            for key in keys:
                self.assertIn(key, body, f"{path}: {key}")

        reminder = await self.client.post(
            "/settings/scan-reminder/check", headers=headers
        )
        self.assertEqual(reminder.status_code, 200)
        self.assertIn("should_notify", reminder.json())

        pdf = await self.client.get("/auth/export/pdf", headers=headers)
        self.assertEqual(pdf.status_code, 200)
        self.assertTrue(pdf.content.startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
