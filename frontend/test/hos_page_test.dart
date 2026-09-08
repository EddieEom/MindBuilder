import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/features/hos/data/hos_repository.dart';
import 'package:frontend/features/hos/presentation/hos_page.dart';
import 'package:frontend/features/growth/application/growth_provider.dart';
import 'package:frontend/features/growth/data/models/growth_model.dart';

final hosFixture = <String, dynamic>{
  'os_id': 3,
  'version': 'v1.0.3',
  'stage': 'Seed',
  'data_confidence': 'High',
  'confidence_score': 87,
  'pattern_scores': {
    'creativity': 84,
    'execution': 67,
    'future': 72,
    'uncertainty': 71,
    'perfectionism': 45,
    'resilience': 66,
  },
  'core_values': [
    {'value_name': '성장', 'description': '꾸준한 학습', 'priority': 1},
  ],
  'thinking_pattern': 'Creative-led',
  'decision_pattern': 'Balanced',
  'operating_rules': ['작은 실천을 우선합니다.'],
  'metadata': {'generated_at': '2026-09-07T09:00:00'},
};
void main() {
  testWidgets('HOS displays charts and loads version history', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          hosProvider.overrideWith(
            (ref) async => HosModel.fromJson(hosFixture),
          ),
          hosVersionsProvider.overrideWith(
            (ref) async => [
              HosVersion.fromJson({
                'os_id': 3,
                'version': 'v1.0.3',
                'stage': 'Seed',
                'generated_at': '2026-09-07T09:00:00',
                'is_current': true,
              }),
            ],
          ),
          growthProvider.overrideWith(
            (ref) async => GrowthModel.fromJson({
              'metadata': {'growth_analysis_id': 1},
              'items': [],
              'recommendations': [],
            }),
          ),
        ],
        child: const MaterialApp(home: HosPage()),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('87'), findsOneWidget);
    expect(find.text('성장'), findsOneWidget);
    await tester.tap(find.text('버전 히스토리'));
    await tester.pumpAndSettle();
    expect(find.text('OS 버전 기록'), findsOneWidget);
    expect(find.text('현재'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
