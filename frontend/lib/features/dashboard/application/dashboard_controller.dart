import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/dio_client.dart';
import '../data/datasources/dashboard_remote_datasource.dart';
import '../data/models/dashboard_model.dart';
import '../data/repositories/dashboard_repository.dart';

final dioClientProvider = Provider<DioClient>((ref) {
  return DioClient();
});

final dashboardRemoteDataSourceProvider =
    Provider<DashboardRemoteDataSource>((ref) {
  final dioClient = ref.watch(dioClientProvider);

  return DashboardRemoteDataSource(dioClient);
});

final dashboardRepositoryProvider =
    Provider<DashboardRepository>((ref) {
  final remoteDataSource =
      ref.watch(dashboardRemoteDataSourceProvider);

  return DashboardRepository(remoteDataSource);
});

final dashboardProvider =
    FutureProvider<DashboardModel>((ref) async {
  final repository =
      ref.watch(dashboardRepositoryProvider);

  return repository.getDashboard();
});