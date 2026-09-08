import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/features/growth/application/growth_provider.dart';
import 'package:frontend/features/growth/data/models/growth_model.dart';
import 'package:frontend/features/growth/presentation/pages/growth_page.dart';
import 'package:frontend/features/lifemap/data/lifemap_repository.dart';
import 'package:frontend/features/lifemap/presentation/lifemap_page.dart';
import 'package:frontend/features/identity/data/identity_repository.dart';
import 'package:frontend/features/identity/presentation/identity_page.dart';
import 'package:frontend/features/hos/data/hos_repository.dart';
import 'package:frontend/features/hos/presentation/hos_page.dart';
import 'package:frontend/features/archive/data/archive_repository.dart';
import 'package:frontend/features/archive/presentation/archive_page.dart';
import 'package:frontend/core/storage/token_storage.dart';
import 'package:frontend/features/auth/application/current_user_provider.dart';
import 'package:frontend/features/auth/data/models/user_profile_model.dart';
import 'package:frontend/features/profile/presentation/profile_page.dart';
import 'package:frontend/features/settings/application/settings_controller.dart';
import 'package:frontend/features/settings/presentation/settings_page.dart';
import 'archive_page_test.dart' show RecordingArchiveRepository;
import 'identity_page_test.dart' show identityFixture;
import 'hos_page_test.dart' show hosFixture;

final visualGrowth = GrowthModel.fromJson({
  'metadata': {
    'growth_analysis_id': 1,
    'confidence': 72,
    'analysis_version': 'rule_v1',
    'created_at': '2026-09-07T09:00:00',
  },
  'items': [
    {
      'type': 'UNLEARNING',
      'title': '학력이나 스펙이 미래를 결정한다.',
      'content': '작은 실행부터 시작해 보세요.',
      'priority': 1,
    },
    {
      'type': 'RELEARNING',
      'title': '불확실성 때문에 미래를 과도하게 시뮬레이션하고 있다.',
      'content': '문제의 원인을 확인해 보세요.',
      'priority': 2,
    },
    {
      'type': 'NEWLEARNING',
      'title': '프로젝트 경험을 성장 가능한 자산으로 전환한다.',
      'content': '경험을 기록해 보세요.',
      'priority': 3,
    },
  ],
  'explanations': [
    {'title': '반복 사고 패턴', 'content': 'Scan 답변의 반복 패턴을 분석했습니다.'},
  ],
  'recommendations': [],
  'feedback': {'rating': 4},
});
final visualMap = LifeMapModel.fromJson({
  'title': 'My Life Map',
  'overview': {
    'interest_count': 1,
    'goal_count': 1,
    'value_count': 1,
    'connection_count': 4,
  },
  'metadata': {'version': 1},
  'nodes': [
    for (final entry in [
      ['1', '나', 'IDENTITY', '#6550F5', 0, 0],
      ['2', '관심사', 'INTEREST', '#66AD7C', 0, -1],
      ['3', '목표', 'GOAL', '#7589EF', 1, 0],
      ['4', '가치관', 'VALUE', '#E6A366', 0, 1],
      ['5', '정체성', 'RELATIONSHIP', '#9B8AFB', -1, 0],
    ])
      {
        'node_id': entry[0],
        'title': entry[1],
        'node_type': entry[2],
        'color': entry[3],
        'x': entry[4],
        'y': entry[5],
        'importance': 80,
        'summary': '',
        'tags': [],
        'related_goals': [],
      },
  ],
  'edges': [
    for (var i = 2; i <= 5; i++) {'from_node': '1', 'to_node': '$i'},
  ],
});

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUpAll(() async {
    final icons = File(
      r'C:\Users\um962\flutter\bin\cache\artifacts\material_fonts\MaterialIcons-Regular.otf',
    );
    if (await icons.exists()) {
      final loader = FontLoader('MaterialIcons')
        ..addFont(
          icons.readAsBytes().then((bytes) => ByteData.sublistView(bytes)),
        );
      await loader.load();
    }
    final font = File(
      Platform.environment['FEATURE_TEST_FONT'] ??
          r'C:\Windows\Fonts\malgun.ttf',
    );
    if (await font.exists()) {
      final loader = FontLoader('FeatureTestFont')
        ..addFont(
          font.readAsBytes().then((bytes) => ByteData.sublistView(bytes)),
        );
      await loader.load();
    }
  });
  final pages = <String, Widget>{
    'growth': const GrowthPage(),
    'lifemap': const LifeMapPage(),
    'identity': const IdentityPage(),
    'hos': const HosPage(),
    'archive': const ArchivePage(),
    'profile': const ProfilePage(),
    'settings': const SettingsPage(),
  };
  for (final entry in pages.entries) {
    testWidgets('${entry.key} mobile layout', (tester) async {
      tester.view.physicalSize = const Size(390, 844);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            growthProvider.overrideWith((ref) async => visualGrowth),
            lifeMapProvider.overrideWith((ref) async => visualMap),
            identityProvider.overrideWith(
              (ref) async => IdentityModel.fromJson(identityFixture),
            ),
            hosProvider.overrideWith(
              (ref) async => HosModel.fromJson(hosFixture),
            ),
            archiveRepositoryProvider.overrideWithValue(
              RecordingArchiveRepository(),
            ),
            currentUserProvider.overrideWith(
              (ref) async => const UserProfileModel(
                email: 'minjun@example.com',
                nickname: '민준',
                profileImage: null,
                identityName: '탐구하는 Builder',
                stage: 'BLUEPRINT',
                provider: 'google',
                scanCount: 124,
                patternCount: 42,
                analysisCount: 87,
                archiveCount: 96,
                goalCount: 23,
              ),
            ),
            settingsProvider.overrideWith(
              (ref) => SettingsController(
                TokenStorage.instance,
                loadStoredValues: false,
              ),
            ),
          ],
          child: MaterialApp(
            theme: ThemeData(
              useMaterial3: true,
              fontFamily: 'FeatureTestFont',
              colorScheme: ColorScheme.fromSeed(
                seedColor: const Color(0xFF6550F5),
              ),
            ),
            home: RepaintBoundary(
              key: const ValueKey('preview'),
              child: entry.value,
            ),
          ),
        ),
      );
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      await expectLater(
        find.byKey(const ValueKey('preview')),
        matchesGoldenFile('../artifacts/previews/${entry.key}.png'),
      );
      tester.view.physicalSize = const Size(320, 700);
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
    });
  }
}
