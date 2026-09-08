import 'dart:convert';
import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/core/network/dio_client.dart';
import 'package:frontend/features/growth/data/datasource/growth_remote_datasource.dart';
import 'package:frontend/features/growth/data/models/growth_model.dart';
import 'package:frontend/features/growth/data/repository/growth_repository.dart';
import 'package:frontend/features/lifemap/data/lifemap_repository.dart';
import 'package:frontend/features/identity/data/identity_repository.dart';
import 'package:frontend/features/hos/data/hos_repository.dart';
import 'package:frontend/features/archive/data/archive_repository.dart';
import 'package:frontend/features/auth/data/repositories/user_profile_repository.dart';
import 'package:frontend/features/settings/data/settings_repository.dart';
import 'lifemap_page_test.dart' show mapFixture;
import 'identity_page_test.dart' show identityFixture;
import 'hos_page_test.dart' show hosFixture;

class RecordingAdapter implements HttpClientAdapter {
  final calls = <RequestOptions>[];
  Object response = <String, dynamic>{};
  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<Uint8List>? stream,
    Future<void>? cancelFuture,
  ) async {
    calls.add(options);
    return ResponseBody.fromString(
      jsonEncode(response),
      200,
      headers: {
        Headers.contentTypeHeader: ['application/json'],
      },
    );
  }

  @override
  void close({bool force = false}) {}
}

void main() {
  test('Growth serializes feedback and next action requests', () async {
    final client = DioClient();
    client.dio.interceptors.clear();
    final adapter = RecordingAdapter();
    client.dio.httpClientAdapter = adapter;
    final repository = GrowthRepository(GrowthRemoteDataSource(client));
    await repository.submitFeedback(12, 5);
    expect(adapter.calls.last.path, '/api/v1/growth/12/feedback');
    expect(adapter.calls.last.method, 'POST');
    expect(adapter.calls.last.data, {'rating': 5});
    await repository.createAction(
      const GrowthRecommendation(
        recommendationId: 7,
        title: '실천',
        description: '작게 시작',
        priority: 1,
      ),
    );
    expect(adapter.calls.last.path, '/api/v1/growth/actions');
    expect(adapter.calls.last.data, {
      'recommendation_id': 7,
      'title': '실천',
      'description': '작게 시작',
    });
  });
  test(
    'detail repositories use registered API paths and parse responses',
    () async {
      final adapter = RecordingAdapter();
      final dio = Dio()..httpClientAdapter = adapter;
      final map = LifeMapRepository(dio);
      adapter.response = mapFixture;
      expect((await map.current()).nodes.first.id, '42');
      expect(adapter.calls.last.path, '/api/v1/lifemap');
      adapter.response = [mapFixture];
      await map.history();
      expect(adapter.calls.last.path, '/api/v1/lifemap/history');
      adapter.response = (mapFixture['nodes'] as List).first;
      await map.node('42');
      expect(adapter.calls.last.path, '/api/v1/lifemap/node/42');
      final identity = IdentityRepository(dio);
      adapter.response = identityFixture;
      expect((await identity.current()).id, 8);
      await identity.detail(8);
      expect(adapter.calls.last.path, '/api/v1/identity/detail/8');
      adapter.response = {'histories': []};
      await identity.history();
      expect(adapter.calls.last.path, '/api/v1/identity/history');
      final hos = HosRepository(dio);
      adapter.response = hosFixture;
      expect((await hos.current()).confidence, 87);
      adapter.response = [hosFixture];
      await hos.history();
      expect(adapter.calls.last.path, '/api/v1/operating-system/history');
      adapter.response = [];
      await hos.versions();
      expect(adapter.calls.last.path, '/api/v1/operating-system/version');
    },
  );
  test('Archive sends tab, date, type and pagination parameters', () async {
    final adapter = RecordingAdapter()..response = {'events': []};
    final repository = ArchiveRepository(Dio()..httpClientAdapter = adapter);
    await repository.events(offset: 30);
    expect(adapter.calls.last.path, '/api/v1/archive/recent');
    expect(adapter.calls.last.queryParameters, {'limit': 30, 'offset': 30});
    await repository.events(tab: 1, date: DateTime(2026, 9, 7));
    expect(adapter.calls.last.path, '/api/v1/archive/calendar');
    expect(adapter.calls.last.queryParameters, {'date': '2026-09-07'});
    await repository.events(tab: 2);
    expect(adapter.calls.last.path, '/api/v1/archive/timeline');
    await repository.events(tab: 3);
    expect(adapter.calls.last.path, '/api/v1/archive/type/OS_UPDATED');
    await repository.events(type: 'IDENTITY_CREATED');
    expect(adapter.calls.last.path, '/api/v1/archive/type/IDENTITY_CREATED');
    adapter.response = {'SCAN_COMPLETED': 3};
    expect(await repository.summary(), {'SCAN_COMPLETED': 3});
  });

  test(
    'Profile reads and mutates the authenticated user through auth APIs',
    () async {
      final client = DioClient();
      client.dio.interceptors.clear();
      final adapter = RecordingAdapter();
      client.dio.httpClientAdapter = adapter;
      final repository = UserProfileRepository(client);

      adapter.response = {
        'email': 'builder@example.com',
        'nickname': '민준',
        'profile_image': 'https://example.com/profile.png',
        'identity_name': '탐구하는 Builder',
        'stage': 'BLUEPRINT',
        'provider': 'google',
        'scan_count': 124,
        'pattern_count': 42,
        'analysis_count': 87,
        'archive_count': 96,
        'goal_count': 23,
      };
      final profile = await repository.getMe();
      expect(profile.nickname, '민준');
      expect(profile.scanCount, 124);
      expect(adapter.calls.last.path, '/auth/me');

      adapter.response = {'nickname': '새 이름'};
      expect(await repository.updateNickname('새 이름'), '새 이름');
      expect(adapter.calls.last.method, 'PATCH');
      expect(adapter.calls.last.path, '/auth/me');
      expect(adapter.calls.last.data, {'nickname': '새 이름'});

      adapter.response = {'profile_image': 'https://example.com/new.png'};
      await repository.updateProfileImage('https://example.com/new.png');
      expect(adapter.calls.last.path, '/auth/profile-image');
      expect(adapter.calls.last.data, {
        'profile_image': 'https://example.com/new.png',
      });

      adapter.response = {
        'user': {'email': 'builder@example.com'},
      };
      expect(await repository.exportData(), contains('builder@example.com'));
      expect(adapter.calls.last.path, '/auth/export');

      adapter.response = [37, 80, 68, 70];
      await repository.exportPdf();
      expect(adapter.calls.last.path, '/auth/export/pdf');
      expect(adapter.calls.last.responseType, ResponseType.bytes);

      adapter.response = {'message': 'deleted'};
      await repository.deleteAccount();
      expect(adapter.calls.last.method, 'DELETE');
      expect(adapter.calls.last.path, '/auth/me');
    },
  );

  test('Settings uses server-backed preferences and reminder API', () async {
    final client = DioClient();
    client.dio.interceptors.clear();
    final adapter = RecordingAdapter();
    client.dio.httpClientAdapter = adapter;
    final repository = SettingsRepository(client);
    adapter.response = {
      'dark_mode': false,
      'language': 'ko',
      'notifications_enabled': true,
      'reminder_hour': 20,
      'timezone': 'Asia/Seoul',
    };
    final settings = await repository.getSettings();
    expect(settings.reminderHour, 20);
    expect(adapter.calls.last.path, '/settings');
    await repository.update({'notifications_enabled': false});
    expect(adapter.calls.last.method, 'PATCH');
    expect(adapter.calls.last.data, {'notifications_enabled': false});

    adapter.response = {
      'should_notify': true,
      'title': '오늘의 Mind Scan',
      'content': '현재 당신의 데이터 신뢰도는 84%입니다.',
      'confidence': 84,
    };
    final reminder = await repository.checkReminder();
    expect(reminder.shouldNotify, isTrue);
    expect(reminder.content, contains('84%'));
    expect(adapter.calls.last.path, '/settings/scan-reminder/check');
  });
}
