import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

import '../config/api_config.dart';
import '../storage/token_storage.dart';

class DioClient {
  DioClient()
      : dio = Dio(
          BaseOptions(
            baseUrl: ApiConfig.baseUrl,
            connectTimeout: ApiConfig.connectTimeout,
            receiveTimeout: ApiConfig.receiveTimeout,
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
          ),
        ),
        _refreshDio = Dio(
          BaseOptions(
            baseUrl: ApiConfig.baseUrl,
            connectTimeout: ApiConfig.connectTimeout,
            receiveTimeout: ApiConfig.receiveTimeout,
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
          ),
        ) {
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final accessToken =
              await TokenStorage.instance.getAccessToken();

          if (accessToken != null &&
              accessToken.isNotEmpty) {
            options.headers['Authorization'] =
                'Bearer $accessToken';

            debugPrint(
              'Authorization token attached',
            );
          } else {
            debugPrint(
              'No access token found',
            );
          }

          handler.next(options);
        },

        onError: (error, handler) async {
          final statusCode = error.response?.statusCode;

          debugPrint(
            'DIO ERROR: $statusCode',
          );

          // 401이 아니면 그대로 에러 전달
          if (statusCode != 401) {
            handler.next(error);
            return;
          }

          // 이미 재시도한 요청이면 무한 루프 방지
          if (error.requestOptions.extra['retry'] == true) {
            debugPrint(
              'Request already retried',
            );

            handler.next(error);
            return;
          }

          try {
            debugPrint(
              '===== ACCESS TOKEN REFRESH START =====',
            );

            final refreshToken =
                await TokenStorage.instance.getRefreshToken();

            if (refreshToken == null ||
                refreshToken.isEmpty) {
              debugPrint(
                'No refresh token found',
              );

              await TokenStorage.instance.clearTokens();

              handler.next(error);
              return;
            }

            // Refresh API 호출
            final refreshResponse =
                await _refreshDio.post(
              '/auth/refresh',
              data: {
                'refresh_token': refreshToken,
              },
            );

            final newAccessToken =
                refreshResponse.data['access_token'];

            final newRefreshToken =
                refreshResponse.data['refresh_token'];

            if (newAccessToken == null ||
                newRefreshToken == null) {
              throw Exception(
                'Token refresh response is invalid',
              );
            }

            // 새 토큰 저장
            await TokenStorage.instance.saveTokens(
              accessToken: newAccessToken,
              refreshToken: newRefreshToken,
            );

            debugPrint(
              '===== ACCESS TOKEN REFRESH SUCCESS =====',
            );

            // 실패했던 요청에 새 Access Token 적용
            final requestOptions =
                error.requestOptions;

            requestOptions.headers['Authorization'] =
                'Bearer $newAccessToken';

            requestOptions.extra['retry'] = true;

            // 기존 요청 재시도
            final response =
                await dio.fetch(requestOptions);

            return handler.resolve(response);
          } catch (e) {
            debugPrint(
              '===== TOKEN REFRESH FAILED =====',
            );

            debugPrint(e.toString());

            // Refresh 실패 → 로그인 상태 제거
            await TokenStorage.instance.clearTokens();

            handler.next(error);
          }
        },
      ),
    );
  }

  final Dio dio;

  final Dio _refreshDio;
}