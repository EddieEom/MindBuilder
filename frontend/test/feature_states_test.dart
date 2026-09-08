import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/features/growth/application/growth_provider.dart';
import 'package:frontend/features/growth/presentation/pages/growth_page.dart';
import 'package:frontend/features/lifemap/data/lifemap_repository.dart';
import 'package:frontend/features/lifemap/presentation/lifemap_page.dart';

void main() {
  testWidgets('request failure displays retry and makes another request', (
    tester,
  ) async {
    var calls = 0;
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          growthProvider.overrideWith((ref) async {
            calls++;
            throw DioException(
              requestOptions: RequestOptions(path: '/api/v1/growth/current'),
            );
          }),
        ],
        child: const MaterialApp(home: GrowthPage()),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('다시 시도'), findsOneWidget);
    await tester.tap(find.text('다시 시도'));
    await tester.pumpAndSettle();
    expect(calls, 2);
    expect(tester.takeException(), isNull);
  });
  testWidgets('empty LifeMap has an explicit empty state', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          lifeMapProvider.overrideWith(
            (ref) async => LifeMapModel.fromJson({
              'title': '',
              'nodes': [],
              'edges': [],
              'overview': {},
              'metadata': {},
            }),
          ),
        ],
        child: const MaterialApp(home: LifeMapPage()),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('Scan을 완료하면 나만의 지도가 만들어져요.'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
