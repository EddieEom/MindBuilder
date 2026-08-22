import '../datasources/dashboard_remote_datasource.dart';
import '../models/dashboard_model.dart';

class DashboardRepository {
  final DashboardRemoteDataSource _remoteDataSource;

  DashboardRepository(this._remoteDataSource);

  Future<DashboardModel> getDashboard() {
    return _remoteDataSource.getDashboard();
  }
}