import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/features/growth/application/growth_provider.dart';
import 'package:frontend/features/growth/data/models/growth_model.dart';
import 'package:frontend/features/growth/data/repository/growth_repository.dart';
import 'package:frontend/features/growth/data/datasource/growth_remote_datasource.dart';
import 'package:frontend/core/network/dio_client.dart';
import 'package:frontend/features/growth/presentation/pages/growth_page.dart';

class RecordingGrowthRepository extends GrowthRepository {
  RecordingGrowthRepository() : super(GrowthRemoteDataSource(DioClient()));
  int? rating;
  int? actionId;
  @override
  Future<void> submitFeedback(int analysisId, int value) async {
    rating = value;
  }

  @override
  Future<void> createAction(GrowthRecommendation recommendation) async {
    actionId = recommendation.recommendationId;
  }
}

void main() {
  final growth = GrowthModel.fromJson({
    'metadata': {
      'growth_analysis_id': 12,
      'confidence': 72,
      'created_at': '2026-09-06T10:00:00',
      'analysis_version': 'rule_v1',
    },
    'items': [
      {
        'type': 'UNLEARNING',
        'title': '작은 실천부터 시작해요',
        'content': '실행의 크기를 줄여 보세요.',
        'priority': 1,
      },
    ],
    'recommendations': [
      {
        'recommendation_id': 5,
        'title': '한 가지 실천',
        'description': '오늘 시작하기',
        'priority': 1,
      },
    ],
    'feedback': {'rating': 3},
  });
  testWidgets('renders API data and submits feedback and action', (
    tester,
  ) async {
    final repository = RecordingGrowthRepository();
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          growthProvider.overrideWith((ref) async => growth),
          growthRepositoryProvider.overrideWithValue(repository),
        ],
        child: const MaterialApp(home: GrowthPage()),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('72%'), findsOneWidget);
    expect(find.text('작은 실천부터 시작해요'), findsOneWidget);
    await tester.ensureVisible(find.text('다음 행동으로 저장'));
    await tester.tap(find.text('다음 행동으로 저장'));
    await tester.pumpAndSettle();
    expect(repository.actionId, 5);
    await tester.ensureVisible(find.byTooltip('5점'));
    await tester.tap(find.byTooltip('5점'));
    await tester.pumpAndSettle();
    expect(repository.rating, 5);
    expect(tester.takeException(), isNull);
  });
}
