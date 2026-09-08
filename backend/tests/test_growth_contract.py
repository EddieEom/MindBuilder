import unittest
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.routers.growth import router
from app.api.dependencies import get_current_user
from app.core.database import get_db


class GrowthContractTests(unittest.TestCase):
    def setUp(self):
        app = FastAPI()
        app.include_router(router, prefix="/api/v1")
        app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(user_id=7)
        app.dependency_overrides[get_db] = lambda: None
        self.client = TestClient(app)
        self.repo = AsyncMock()
        self.patcher = patch("app.api.routers.growth.GrowthRepository", return_value=self.repo)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_feedback_validates_rating(self):
        for rating in (0, 6):
            response = self.client.post('/api/v1/growth/12/feedback', json={'rating': rating})
            self.assertEqual(response.status_code, 422)
        self.repo.upsert_feedback.assert_not_called()

    def test_feedback_updates_existing_record(self):
        self.repo.get_owned_analysis.return_value = SimpleNamespace(growth_analysis_id=12)
        self.repo.upsert_feedback.return_value = SimpleNamespace(feedback_id=2, rating=4, comment=None)
        for _ in range(2):
            response = self.client.post('/api/v1/growth/12/feedback', json={'rating': 4})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['feedback_id'], 2)
        self.repo.get_owned_analysis.assert_awaited_with(12, 7)
        self.repo.create_feedback.assert_not_called()

    def test_feedback_rejects_other_user_analysis(self):
        self.repo.get_owned_analysis.return_value = None
        response = self.client.post('/api/v1/growth/12/feedback', json={'rating': 4})
        self.assertEqual(response.status_code, 404)
        self.repo.upsert_feedback.assert_not_called()

    def test_action_returns_existing_action(self):
        self.repo.get_actions.return_value = [SimpleNamespace(action_id=3, status='WAITING', created_at=datetime(2026, 9, 6))]
        response = self.client.post('/api/v1/growth/actions', json={'recommendation_id': 5, 'title': '작은 실천'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['action_id'], 3)
        self.repo.create_next_action.assert_not_called()

    def test_action_rejects_other_user_recommendation(self):
        self.repo.get_owned_recommendation.return_value = None
        response = self.client.post('/api/v1/growth/actions', json={'recommendation_id': 5, 'title': '작은 실천'})
        self.assertEqual(response.status_code, 404)
        self.repo.create_next_action.assert_not_called()

    def test_creates_action_for_owned_recommendation(self):
        self.repo.get_actions.return_value = []
        self.repo.create_next_action.return_value = SimpleNamespace(action_id=4, status='WAITING', created_at=datetime(2026, 9, 6))
        response = self.client.post('/api/v1/growth/actions', json={'recommendation_id': 5, 'title': '작은 실천'})
        self.assertEqual(response.status_code, 200)
        action = self.repo.create_next_action.call_args.args[0]
        self.assertEqual(action.user_id, 7)
        self.assertEqual(action.recommendation_id, 5)
        self.repo.commit.assert_awaited_once()


if __name__ == '__main__':
    unittest.main()
