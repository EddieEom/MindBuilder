import 'package:dio/dio.dart';

import '../../../../core/network/dio_client.dart';

class AuthRepository {
  AuthRepository({DioClient? dioClient})
    : _dio = (dioClient ?? DioClient()).dio;

  final Dio _dio;

  Future<Map<String, dynamic>> loginWithOAuth({
    required String email,
    required String nickname,
    required String provider,
    required String providerUserId,
    required String profileImage,
  }) async {
    final response = await _dio.post(
      '/auth/login/oauth',
      data: {
        'email': email,
        'nickname': nickname,
        'provider': provider,
        'provider_user_id': providerUserId,
        'profile_image': profileImage,
      },
    );

    return Map<String, dynamic>.from(response.data);
  }
}
