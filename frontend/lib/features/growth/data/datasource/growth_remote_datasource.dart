import '../../../../core/network/dio_client.dart';

class GrowthRemoteDataSource {
  Future<void> submitFeedback(int analysisId, int rating) async {
    await dioClient.dio.post(
      '/api/v1/growth/$analysisId/feedback',
      data: {'rating': rating},
    );
  }

  Future<void> createAction(
    int recommendationId,
    String title,
    String description,
  ) async {
    await dioClient.dio.post(
      '/api/v1/growth/actions',
      data: {
        'recommendation_id': recommendationId,
        'title': title,
        'description': description,
      },
    );
  }

  final DioClient dioClient;

  GrowthRemoteDataSource(this.dioClient);

  Future<Map<String, dynamic>> getCurrentGrowth() async {
    final response = await dioClient.dio.get('/api/v1/growth/current');

    return response.data;
  }
}
