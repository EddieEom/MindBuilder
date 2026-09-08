import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/features/archive/data/archive_repository.dart';
import 'package:frontend/features/archive/presentation/archive_page.dart';

class RecordingArchiveRepository extends ArchiveRepository {
  RecordingArchiveRepository() : super(Dio());
  final List<({int tab, String? type, int offset})> calls = [];
  @override
  Future<List<ArchiveEvent>> events({
    int tab = 0,
    DateTime? date,
    String? type,
    int offset = 0,
  }) async {
    calls.add((tab: tab, type: type, offset: offset));
    return [
      ArchiveEvent.fromJson({
        'event_id': 1,
        'reference_id': 1,
        'event_type': tab == 3 ? 'OS_UPDATED' : 'GROWTH_ANALYZED',
        'title': tab == 3 ? 'Human OS 업데이트' : 'Growth 분석 결과',
        'summary': '작은 행동으로 시작해요',
        'created_at': '2026-09-07T09:00:00',
      }),
    ];
  }

  @override
  Future<Map<String, int>> summary() async => {
    'SCAN_COMPLETED': 124,
    'GROWTH_ANALYZED': 96,
    'OS_UPDATED': 67,
  };
}

void main() {
  testWidgets('archive tabs request their endpoints and display details', (
    tester,
  ) async {
    final repository = RecordingArchiveRepository();
    await tester.pumpWidget(
      ProviderScope(
        overrides: [archiveRepositoryProvider.overrideWithValue(repository)],
        child: const MaterialApp(home: ArchivePage()),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('124'), findsOneWidget);
    await tester.tap(find.text('성장 타임라인'));
    await tester.pumpAndSettle();
    expect(repository.calls.last.tab, 2);
    await tester.tap(find.text('최근 HOS'));
    await tester.pumpAndSettle();
    expect(repository.calls.last.tab, 3);
    await tester.tap(find.text('Human OS 업데이트'));
    await tester.pumpAndSettle();
    expect(find.text('작은 행동으로 시작해요'), findsWidgets);
    expect(tester.takeException(), isNull);
  });
}
