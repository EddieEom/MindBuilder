import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/storage/token_storage.dart';
import '../data/settings_repository.dart';

class SettingsState {
  const SettingsState({
    this.darkMode = false,
    this.language = 'ko',
    this.notifications = true,
    this.reminderHour = 20,
  });
  final bool darkMode;
  final String language;
  final bool notifications;
  final int reminderHour;
  SettingsState copyWith({
    bool? darkMode,
    String? language,
    bool? notifications,
    int? reminderHour,
  }) => SettingsState(
    darkMode: darkMode ?? this.darkMode,
    language: language ?? this.language,
    notifications: notifications ?? this.notifications,
    reminderHour: reminderHour ?? this.reminderHour,
  );
}

class SettingsController extends StateNotifier<SettingsState> {
  SettingsController(
    this.storage, {
    this.repository,
    bool loadStoredValues = true,
  }) : super(const SettingsState()) {
    if (loadStoredValues) {
      _load();
    }
  }
  final TokenStorage storage;
  final SettingsRepository? repository;
  Future<void> _load() async {
    state = SettingsState(
      darkMode: await storage.getDarkMode(),
      language: await storage.getLanguage(),
      notifications: await storage.getNotifications(),
    );
    try {
      final remote = await repository?.getSettings();
      if (remote == null) return;
      state = SettingsState(
        darkMode: remote.darkMode,
        language: remote.language,
        notifications: remote.notificationsEnabled,
        reminderHour: remote.reminderHour,
      );
      await storage.saveDarkMode(remote.darkMode);
      await storage.saveLanguage(remote.language);
      await storage.saveNotifications(remote.notificationsEnabled);
    } catch (_) {
      // Keep the cached settings while offline.
    }
  }

  Future<void> setDarkMode(bool value) async {
    state = state.copyWith(darkMode: value);
    await storage.saveDarkMode(value);
    await repository?.update({'dark_mode': value});
  }

  Future<void> setLanguage(String value) async {
    state = state.copyWith(language: value);
    await storage.saveLanguage(value);
    await repository?.update({'language': value});
  }

  Future<void> setNotifications(bool value) async {
    state = state.copyWith(notifications: value);
    await storage.saveNotifications(value);
    await repository?.update({'notifications_enabled': value});
  }

  Future<void> setReminderHour(int value) async {
    state = state.copyWith(reminderHour: value);
    await repository?.update({'reminder_hour': value});
  }
}

final settingsProvider =
    StateNotifierProvider<SettingsController, SettingsState>(
      (ref) => SettingsController(
        TokenStorage.instance,
        repository: ref.watch(settingsRepositoryProvider),
      ),
    );
