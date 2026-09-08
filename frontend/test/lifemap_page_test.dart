import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:frontend/features/lifemap/data/lifemap_repository.dart';
import 'package:frontend/features/lifemap/presentation/lifemap_page.dart';

final mapFixture = <String, dynamic>{
  'title': 'My Life Map',
  'overview': {
    'interest_count': 1,
    'goal_count': 0,
    'value_count': 0,
    'connection_count': 0,
  },
  'metadata': {'version': 1, 'generated_at': '2026-09-07T09:00:00'},
  'nodes': [
    {
      'node_id': '42',
      'title': '관심사',
      'node_type': 'INTEREST',
      'importance': 80,
      'color': '#66AD7C',
      'summary': '관심사 요약',
      'x': 0,
      'y': 0,
      'tags': [
        {'name': 'AI'},
      ],
      'related_goals': [
        {'title': '학습 시작', 'progress': 40, 'status': 'IN_PROGRESS'},
      ],
    },
  ],
  'edges': [],
};

void main() {
  testWidgets('map tabs and node detail display API values', (tester) async {
    final map = LifeMapModel.fromJson(mapFixture);
    final router = GoRouter(
      initialLocation: '/lifemap',
      routes: [
        GoRoute(path: '/lifemap', builder: (_, _) => const LifeMapPage()),
        GoRoute(
          path: '/lifemap/node/:id',
          builder: (_, state) =>
              LifeMapNodePage(nodeId: state.pathParameters['id']!),
        ),
      ],
    );
    addTearDown(router.dispose);
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          lifeMapProvider.overrideWith((ref) async => map),
          lifeMapHistoryProvider.overrideWith((ref) async => [map]),
          lifeMapNodeProvider(
            '42',
          ).overrideWith((ref) async => map.nodes.first),
        ],
        child: MaterialApp.router(routerConfig: router),
      ),
    );
    await tester.pumpAndSettle();
    await tester.tap(find.text('연결 지도'));
    await tester.pumpAndSettle();
    expect(find.byTooltip('확대'), findsOneWidget);
    await tester.tap(find.byTooltip('확대'));
    await tester.pumpAndSettle();
    await tester.tap(find.byTooltip('지도 초기화'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('관심사'));
    await tester.pumpAndSettle();
    expect(find.text('노드 상세'), findsOneWidget);
    expect(find.text('AI'), findsOneWidget);
    expect(find.text('40%'), findsOneWidget);
    router.pop();
    await tester.pumpAndSettle();
    await tester.tap(find.text('히스토리'));
    await tester.pumpAndSettle();
    expect(find.text('Life Map v1'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
