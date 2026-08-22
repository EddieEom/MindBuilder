import 'package:dio/dio.dart';

import '../models/oauth_login_request.dart';
import '../models/oauth_login_response.dart';

class AuthRemoteDataSource {
  final Dio dio;

  AuthRemoteDataSource(this.dio);

  Future<OAuthLoginResponse> oauthLogin(
    OAuthLoginRequest request,
  ) async {
    final response = await dio.post(
      '/auth/login/oauth',
      data: request.toJson(),
    );

    return OAuthLoginResponse.fromJson(
      response.data,
    );
  }
}