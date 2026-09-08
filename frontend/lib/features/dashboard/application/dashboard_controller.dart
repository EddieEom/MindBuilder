import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter/material.dart';

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

  debugPrint("=== DASHBOARD PROVIDER START ===");

  final repository =
      ref.watch(dashboardRepositoryProvider);

  debugPrint("=== CALL API ===");

  final result = await repository.getDashboard();

  debugPrint("=== DASHBOARD RESULT ===");
  debugPrint(result.toString());

  return result;
});