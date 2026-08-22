import '../../../../core/network/dio_client.dart';
import '../models/dashboard_model.dart';

class DashboardRemoteDataSource {
  final DioClient _dioClient;

  DashboardRemoteDataSource(this._dioClient);

  Future<DashboardModel> getDashboard() async {
    final response = await _dioClient.dio.get(
      '/api/v1/dashboard',
    );

    return DashboardModel.fromJson(
      response.data as Map<String, dynamic>,
    );
  }
}