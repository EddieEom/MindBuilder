import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class TokenStorage {
  TokenStorage._();

  static final TokenStorage instance = TokenStorage._();

  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  static const _accessTokenKey = 'access_token';
  static const _refreshTokenKey = 'refresh_token';
  static const _darkModeKey = 'dark_mode';
  static const _languageKey = 'language';
  static const _notificationsKey = 'notifications';

  Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    await _storage.write(key: _accessTokenKey, value: accessToken);

    await _storage.write(key: _refreshTokenKey, value: refreshToken);
  }

  Future<String?> getAccessToken() async {
    return _storage.read(key: _accessTokenKey);
  }

  Future<String?> getRefreshToken() async {
    return _storage.read(key: _refreshTokenKey);
  }

  Future<void> clearTokens() async {
    await _storage.delete(key: _accessTokenKey);

    await _storage.delete(key: _refreshTokenKey);
  }

  Future<bool> getDarkMode() async =>
      (await _storage.read(key: _darkModeKey)) == 'true';

  Future<void> saveDarkMode(bool enabled) =>
      _storage.write(key: _darkModeKey, value: '$enabled');

  Future<String> getLanguage() async =>
      await _storage.read(key: _languageKey) ?? 'ko';

  Future<void> saveLanguage(String language) =>
      _storage.write(key: _languageKey, value: language);

  Future<bool> getNotifications() async =>
      (await _storage.read(key: _notificationsKey)) != 'false';

  Future<void> saveNotifications(bool enabled) =>
      _storage.write(key: _notificationsKey, value: '$enabled');
}
