"""API/database integration checks. All mutations are rolled back."""
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.core.database import engine, get_db
from app.api.dependencies import get_current_user
from app.features.auth.dependencies import get_current_user as get_auth_current_user
from app.models.scan import Scan
from app.models.analysis import PatternAnalysis
from app.models.growth import GrowthAnalysis
from app.models.user import OAuthAccount, User
from app.models.scan import FeatureObservation, FeatureValue
from app.ai.feature_extractor.feature_result import FeatureResult
from app.repositories.feature_repository import FeatureRepository
from app.services.seed_initialization_service import SeedInitializationService


class FeatureDatabaseTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        engine.echo = False
        self.connection = await engine.connect()
        self.transaction = await self.connection.begin()
        self.session = AsyncSession(bind=self.connection, expire_on_commit=False, join_transaction_mode='create_savepoint')
        user_id = (await self.session.execute(select(Scan.user_id).join(PatternAnalysis, PatternAnalysis.scan_id == Scan.scan_id).join(GrowthAnalysis, GrowthAnalysis.pattern_id == PatternAnalysis.pattern_id).order_by(GrowthAnalysis.created_at.desc()).limit(1))).scalar_one_or_none()
        if user_id is None:
            await self.session.close()
            await self.transaction.rollback()
            await self.connection.close()
            await engine.dispose()
            self.skipTest('No stored Growth analysis available for database integration')
        self.owner = SimpleNamespace(user_id=user_id)
        async def database():
            yield self.session
        app.dependency_overrides[get_db] = database
        app.dependency_overrides[get_current_user] = lambda: self.owner
        app.dependency_overrides[get_auth_current_user] = lambda: self.owner
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test')

    async def asyncTearDown(self):
        app.dependency_overrides.clear()
        await self.client.aclose()
        await self.session.close()
        await self.transaction.rollback()
        await self.connection.close()
        await engine.dispose()

    async def get(self, path):
        response = await self.client.get('/api/v1/' + path)
        self.assertEqual(response.status_code, 200, path)
        return response.json()

    async def test_growth_feedback_roundtrip(self):
        growth = await self.get('growth/current')
        analysis_id = growth['metadata']['growth_analysis_id']
        ids = []
        for rating in (4, 5):
            response = await self.client.post(f'/api/v1/growth/{analysis_id}/feedback', json={'rating': rating, 'comment': 'Integration test; rolled back'})
            self.assertEqual(response.status_code, 200)
            ids.append(response.json()['feedback_id'])
            current = await self.get('growth/current')
            self.assertEqual(current['feedback']['rating'], rating)
        self.assertEqual(ids[0], ids[1])
        invalid = await self.client.post(f'/api/v1/growth/{analysis_id}/feedback', json={'rating': 6})
        self.assertEqual(invalid.status_code, 422)
        await self.get(f'growth/{analysis_id}')
        self.owner = SimpleNamespace(user_id=-1)
        forbidden = await self.client.post(f'/api/v1/growth/{analysis_id}/feedback', json={'rating': 4})
        self.assertEqual(forbidden.status_code, 404)

    async def test_action_roundtrip(self):
        growth = await self.get('growth/current')
        self.assertTrue(growth['recommendations'], 'Expected stored recommendations')
        recommendation = growth['recommendations'][0]
        payload = {'recommendation_id': recommendation['recommendation_id'], 'title': recommendation['title'], 'description': recommendation['description']}
        first = await self.client.post('/api/v1/growth/actions', json=payload)
        second = await self.client.post('/api/v1/growth/actions', json=payload)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.json()['action_id'], second.json()['action_id'])
        self.owner = SimpleNamespace(user_id=-1)
        forbidden = await self.client.post('/api/v1/growth/actions', json=payload)
        self.assertEqual(forbidden.status_code, 404)

    async def test_lifemap_and_identity(self):
        life_map = await self.get('lifemap')
        await self.get('lifemap/history')
        self.assertTrue(life_map['nodes'], 'Expected stored LifeMap nodes')
        node_id = life_map['nodes'][0]['node_id']
        await self.get(f'lifemap/node/{node_id}')
        identity = await self.get('identity/current')
        await self.get('identity/history')
        identity_id = identity['metadata']['identity_id']
        await self.get(f'identity/detail/{identity_id}')
        feedback = await self.client.post(
            f'/api/v1/identity/{identity_id}/feedback',
            json={'agreement': 'PARTIAL', 'correction_text': 'I also value careful exploration.'},
        )
        self.assertEqual(feedback.status_code, 200)
        current = await self.get('identity/current')
        self.assertEqual(current['feedback']['agreement'], 'PARTIAL')
        self.assertIn('candidates', current)
        invalid = await self.client.post(
            f'/api/v1/identity/{identity_id}/feedback', json={'agreement': 'DISAGREE'}
        )
        self.assertEqual(invalid.status_code, 422)
        self.owner = SimpleNamespace(user_id=-1)
        for path in (f'lifemap/node/{node_id}', f'identity/detail/{identity_id}'):
            response = await self.client.get('/api/v1/' + path)
            self.assertEqual(response.status_code, 404)

    async def test_adaptive_questions_prioritize_low_confidence_features(self):
        response = await self.client.get('/api/v1/onboarding/adaptive/questions?limit=3')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['adaptive'])
        self.assertLessEqual(len(payload['questions']), 3)
        self.assertTrue(payload['questions'])
        self.assertIn('information_need', payload['questions'][0])
        self.assertIn('target_features', payload['questions'][0])

    async def test_repeated_scan_feedback_journey(self):
        questions = (await self.get('onboarding/questions'))['questions']

        async def complete(selected):
            started = await self.client.post('/api/v1/onboarding/start')
            self.assertEqual(started.status_code, 200, started.text)
            scan_id = started.json()['scan_id']
            response = await self.client.post('/api/v1/onboarding/answers', json={
                'scan_id': scan_id,
                'answers': [{
                    'question_id': q['question_id'],
                    'option_id': q['options'][6 if len(selected) > 1 and q['question_id'] == 2 else 0]['option_id'],
                    'point_value': 100 if q['question_type'] == 'POINT' else 0,
                } for q in selected],
            })
            self.assertEqual(response.status_code, 200, response.text)
            return scan_id, response.json()

        _, first = await complete(questions)
        identity_id = first['identity']['metadata']['identity_id']
        correction = '실행 결과보다 충분히 탐색하는 과정을 중요하게 생각합니다.'
        feedback = await self.client.post(f'/api/v1/identity/{identity_id}/feedback', json={
            'agreement': 'PARTIAL', 'correction_text': correction,
        })
        self.assertEqual(feedback.status_code, 200, feedback.text)
        for _ in range(2):
            selected = (await self.get('onboarding/adaptive/questions?limit=1'))['questions']
            self.assertIn(correction, selected[0]['description'])
            scan_id, result = await complete(selected)
            self.assertEqual(result['identity']['hypothesis_status'], 'REVIEW_REQUIRED')
            self.assertEqual(result['identity']['user_perspective']['provenance'], 'USER_CLAIM')
            carried = result['metadata']['carried_features']
            self.assertTrue(carried, str(result['metadata']) + str(selected))
            observations = (await self.session.execute(
                select(FeatureObservation).where(FeatureObservation.scan_id == scan_id)
            )).scalars().all()
            self.assertFalse(any(row.feature_code in carried for row in observations))
            current = await self.get('identity/current')
            self.assertEqual(current['hypothesis_status'], 'REVIEW_REQUIRED')
            self.assertEqual(current['user_perspective']['correction_text'], correction)
            self.assertTrue(current['candidates'])

    async def test_hos_and_archive(self):
        os = await self.get('operating-system/current')
        self.assertEqual(len(os['pattern_scores']), 6)
        await self.get('operating-system/history')
        await self.get('operating-system/version')
        summary = await self.get('archive/summary')
        self.assertGreater(sum(summary.values()), 0)
        first = await self.get('archive/recent?limit=1&offset=0')
        second = await self.get('archive/recent?limit=1&offset=1')
        if first['events'] and second['events']:
            self.assertNotEqual(first['events'][0]['event_id'], second['events'][0]['event_id'])
        if first['events']:
            date = first['events'][0]['created_at'][:10]
            await self.get(f'archive/calendar?date={date}')
        await self.get('archive/type/OS_UPDATED?offset=0')
        await self.get('archive/timeline?offset=0')

    async def test_profile_management_roundtrip(self):
        profile_response = await self.client.get('/auth/me')
        self.assertEqual(profile_response.status_code, 200)
        profile = profile_response.json()
        self.assertEqual(profile['email'], (await self.session.get(User, self.owner.user_id)).email)
        self.assertIn('scan_count', profile)
        self.assertIn('identity_name', profile)

        oauth = (await self.session.execute(
            select(OAuthAccount).where(OAuthAccount.user_id == self.owner.user_id).limit(1)
        )).scalar_one_or_none()
        if oauth is not None:
            login = await self.client.post('/auth/login/oauth', json={
                'email': oauth.provider_email,
                'nickname': profile['nickname'],
                'provider': oauth.provider,
                'provider_user_id': oauth.provider_user_id,
                'profile_image': profile['profile_image'],
            })
            self.assertEqual(login.status_code, 200)
            self.assertFalse(login.json()['is_new_user'])

        nickname = await self.client.patch('/auth/me', json={'nickname': '통합테스트'})
        self.assertEqual(nickname.status_code, 200)
        self.assertEqual(nickname.json()['nickname'], '통합테스트')

        image_url = 'https://example.com/profile.png'
        image = await self.client.patch('/auth/profile-image', json={'profile_image': image_url})
        self.assertEqual(image.status_code, 200)
        self.assertEqual(image.json()['profile_image'], image_url)
        invalid_image = await self.client.patch('/auth/profile-image', json={'profile_image': 'file:///profile.png'})
        self.assertEqual(invalid_image.status_code, 422)

        export_response = await self.client.get('/auth/export')
        self.assertEqual(export_response.status_code, 200)
        exported = export_response.json()
        self.assertIn('user', exported)
        self.assertIn('growth', exported)
        pdf = await self.client.get('/auth/export/pdf')
        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf.headers['content-type'], 'application/pdf')
        self.assertTrue(pdf.content.startswith(b'%PDF'))

        deleted = await self.client.delete('/auth/me')
        self.assertEqual(deleted.status_code, 200)
        self.assertIsNone(await self.session.get(User, self.owner.user_id))

    async def test_settings_and_daily_scan_reminder(self):
        initial = await self.client.get('/settings')
        self.assertEqual(initial.status_code, 200)
        self.assertEqual(initial.json()['timezone'], 'Asia/Seoul')

        updated = await self.client.patch('/settings', json={
            'dark_mode': True,
            'language': 'ko',
            'notifications_enabled': True,
            'reminder_hour': 0,
        })
        self.assertEqual(updated.status_code, 200)
        self.assertTrue(updated.json()['dark_mode'])
        self.assertEqual(updated.json()['reminder_hour'], 0)
        invalid = await self.client.patch('/settings', json={'reminder_hour': 24})
        self.assertEqual(invalid.status_code, 422)

        first = await self.client.post('/settings/scan-reminder/check')
        self.assertEqual(first.status_code, 200)
        self.assertTrue(first.json()['should_notify'])
        self.assertIn('데이터 신뢰도는', first.json()['content'])
        second = await self.client.post('/settings/scan-reminder/check')
        self.assertEqual(second.status_code, 200)
        self.assertFalse(second.json()['should_notify'])

    async def test_feature_evidence_persistence_and_quality_score(self):
        combined = FeatureResult()
        combined.add_confidence('future_score', .8)
        combined.add_confidence('future_score', .7)
        self.assertAlmostEqual(combined.get_confidence('future_score'), .94)

        scan = Scan(
            user_id=self.owner.user_id,
            scan_type='ONBOARDING',
            started_at=datetime.now(timezone.utc).replace(tzinfo=None),
            completed_at=datetime.now(timezone.utc).replace(tzinfo=None),
            status='COMPLETED',
        )
        self.session.add(scan)
        await self.session.flush()
        result = FeatureResult(
            scores={'future_score': 70, 'execution_score': 55},
            confidence={'future_score': .8, 'execution_score': .7},
            evidences={
                'future_score': [{'rule_id': 'Q1_FUTURE', 'confidence': .8, 'direction': 'positive'}],
                'execution_score': [{'rule_id': 'Q2_EXECUTION', 'confidence': .7, 'direction': 'positive'}],
            },
            conflicts=[{'rule_id': 'C1', 'gap': 'future_execution', 'severity': 'MEDIUM'}],
        )
        result.initialize_scores([
            'creativity_score', 'uncertainty_score', 'perfectionism_score',
            'resilience_score', 'overload_score',
        ])
        repository = FeatureRepository(self.session)
        await repository.create(scan.scan_id, result)
        metrics = await repository.quality_metrics(scan.scan_id, self.owner.user_id)
        values = list((await self.session.execute(
            select(FeatureValue).where(FeatureValue.scan_id == scan.scan_id)
        )).scalars())
        observations = list((await self.session.execute(
            select(FeatureObservation).where(FeatureObservation.scan_id == scan.scan_id)
        )).scalars())
        self.assertEqual(len(values), 7)
        self.assertEqual(len(observations), 3)
        self.assertAlmostEqual(metrics['evidence_strength'], .75)
        self.assertEqual(metrics['conflict_strength'], .5)
        score = SeedInitializationService(self.session)._calculate_confidence_score(
            answer_question_count=6,
            feature_count=2,
            other_input_count=1,
            evidence_count=2,
            evidence_strength=metrics['evidence_strength'],
            conflict_strength=metrics['conflict_strength'],
            longitudinal_stability=metrics['stability'],
        )
        self.assertGreaterEqual(score, 10)
        self.assertLessEqual(score, 95)


if __name__ == '__main__':
    unittest.main()
