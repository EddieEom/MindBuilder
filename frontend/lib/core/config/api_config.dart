class ApiConfig {
  ApiConfig._();

  static const String baseUrl = 'http://192.168.0.12:8000';

  static const Duration connectTimeout = Duration(seconds: 10);
  static const Duration receiveTimeout = Duration(seconds: 15);
}