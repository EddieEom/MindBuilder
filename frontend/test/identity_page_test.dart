import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:frontend/features/identity/data/identity_repository.dart';
import 'package:frontend/features/identity/presentation/identity_page.dart';

final identityFixture = <String, dynamic>{
  'identity_name': '탐구하는 Builder',
  'description': '질문하며 배우고 성장하는 사람',
  'confidence': 75,
  'creativity_score': 84,
  'execution_score': 67,
  'uncertainty_score': 71,
  'keywords': ['탐구자', '문제해결자'],
  'strengths': ['새로운 아이디어를 연결함'],
  'growth_points': ['작은 실행을 시작하기'],
  'metadata': {
    'identity_id': 8,
    'version': 2,
    'generated_at': '2026-09-07T09:00:00',
  },
  'evidence': {},
};
void main() {
  testWidgets('identity renders scores and opens API detail', (tester) async {
    final model = IdentityModel.fromJson(identityFixture);
    final router = GoRouter(
      initialLocation: '/identity',
      routes: [
        GoRoute(path: '/identity', builder: (_, _) => const IdentityPage()),
        GoRoute(
          path: '/identity/:id',
          builder: (_, state) =>
              IdentityPage(identityId: int.parse(state.pathParameters['id']!)),
        ),
      ],
    );
    addTearDown(router.dispose);
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          identityProvider.overrideWith((ref) async => model),
          identityDetailProvider(8).overrideWith((ref) async => model),
        ],
        child: MaterialApp.router(routerConfig: router),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('84'), findsOneWidget);
    expect(find.text('탐구자'), findsOneWidget);
    await tester.scrollUntilVisible(find.text('더 자세히 보기'), 200);
    await tester.tap(find.text('더 자세히 보기'));
    await tester.pumpAndSettle();
    expect(find.text('Identity 상세'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
