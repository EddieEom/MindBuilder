import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/app_provider.dart';
import '../data/datasource/growth_remote_datasource.dart';
import '../data/repository/growth_repository.dart';
import '../data/models/growth_model.dart';

final growthRemoteDataSourceProvider = Provider((ref) {
  return GrowthRemoteDataSource(ref.watch(dioProvider));
});

final growthRepositoryProvider = Provider((ref) {
  return GrowthRepository(ref.watch(growthRemoteDataSourceProvider));
});

final growthProvider = FutureProvider.autoDispose<GrowthModel>((ref) async {
  final repository = ref.watch(growthRepositoryProvider);

  return repository.getCurrentGrowth();
});
