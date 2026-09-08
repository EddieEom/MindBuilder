import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/app_provider.dart';
import '../../../core/network/dio_client.dart';

class RemoteSettings {
  const RemoteSettings({
    required this.darkMode,
    required this.language,
    required this.notificationsEnabled,
    required this.reminderHour,
    required this.timezone,
  });

  final bool darkMode;
  final String language;
  final bool notificationsEnabled;
  final int reminderHour;
  final String timezone;

  factory RemoteSettings.fromJson(Map<String, dynamic> json) => RemoteSettings(
    darkMode: json['dark_mode'] as bool,
    language: json['language'] as String,
    notificationsEnabled: json['notifications_enabled'] as bool,
    reminderHour: (json['reminder_hour'] as num).toInt(),
    timezone: json['timezone'] as String,
  );
}

class ScanReminder {
  const ScanReminder({required this.shouldNotify, this.title, this.content});
  final bool shouldNotify;
  final String? title;
  final String? content;

  factory ScanReminder.fromJson(Map<String, dynamic> json) => ScanReminder(
    shouldNotify: json['should_notify'] as bool,
    title: json['title'] as String?,
    content: json['content'] as String?,
  );
}

class SettingsRepository {
  SettingsRepository(this.client);
  final DioClient client;

  Future<RemoteSettings> getSettings() async {
    final response = await client.dio.get('/settings');
    return RemoteSettings.fromJson(response.data as Map<String, dynamic>);
  }

  Future<RemoteSettings> update(Map<String, dynamic> values) async {
    final response = await client.dio.patch('/settings', data: values);
    return RemoteSettings.fromJson(response.data as Map<String, dynamic>);
  }

  Future<ScanReminder> checkReminder() async {
    final response = await client.dio.post('/settings/scan-reminder/check');
    return ScanReminder.fromJson(response.data as Map<String, dynamic>);
  }
}

final settingsRepositoryProvider = Provider<SettingsRepository>(
  (ref) => SettingsRepository(ref.watch(dioProvider)),
);
