import 'package:dio/dio.dart';

import '../../../../core/network/dio_client.dart';
import '../models/onboarding_question_model.dart';

class OnboardingRepository {
  OnboardingRepository({
    Dio? dio,
  }) : _dio = dio ?? DioClient().dio;

  final Dio _dio;

  Future<OnboardingQuestionSet> getQuestions() async {
    final response = await _dio.get(
      '/api/v1/onboarding/questions',
    );

    return OnboardingQuestionSet.fromJson(
      response.data as Map<String, dynamic>,
    );
  }

  Future<int> startOnboarding() async {
    final response = await _dio.post(
      '/api/v1/onboarding/start',
    );

    return response.data['scan_id'] as int;
  }

  Future<Map<String, dynamic>> submitAnswers({
    required int scanId,
    required List<Map<String, dynamic>> answers,
  }) async {
    final response = await _dio.post(
      '/api/v1/onboarding/answers',
      data: {
        'scan_id': scanId,
        'answers': answers,
      },
    );

    return Map<String, dynamic>.from(
      response.data as Map,
    );
  }

  Future<Map<String, dynamic>> analyzePattern({
    required int scanId,
  }) async {
    final response = await _dio.post(
      '/api/v1/pattern/pattern/analyze',
      data: {
        'scan_id': scanId,
      },
    );

    return Map<String, dynamic>.from(
      response.data as Map,
    );
}

  
}