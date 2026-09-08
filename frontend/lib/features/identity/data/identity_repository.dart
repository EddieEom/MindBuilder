import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../app/app_provider.dart';

class IdentityModel {
  IdentityModel.fromJson(Map<String, dynamic> json)
    : name = json['identity_name'] as String,
      description = json['description'] as String,
      confidence = (json['confidence'] as num).toDouble(),
      creativity = (json['creativity_score'] as num).toDouble(),
      execution = (json['execution_score'] as num).toDouble(),
      uncertainty = (json['uncertainty_score'] as num).toDouble(),
      keywords = List<String>.from(json['keywords']),
      strengths = List<String>.from(json['strengths']),
      growthPoints = List<String>.from(json['growth_points']),
      metadata = Map<String, dynamic>.from(json['metadata'] ?? {}),
      evidence = Map<String, dynamic>.from(json['evidence'] ?? {});
  final String name, description;
  final double confidence, creativity, execution, uncertainty;
  final List<String> keywords, strengths, growthPoints;
  final Map<String, dynamic> metadata, evidence;
  int? get id => (metadata['identity_id'] as num?)?.toInt();
}

class IdentityHistory {
  IdentityHistory.fromJson(Map<String, dynamic> json)
    : id = json['identity_id'] as int,
      name = json['identity_name'] as String,
      version = json['version'] as int,
      date = DateTime.parse(json['generated_at'] as String),
      current = json['is_current'] as bool;
  final int id, version;
  final String name;
  final DateTime date;
  final bool current;
}

class IdentityRepository {
  IdentityRepository(this.dio);
  final Dio dio;
  Future<IdentityModel> current() async => IdentityModel.fromJson(
    Map<String, dynamic>.from((await dio.get('/api/v1/identity/current')).data),
  );
  Future<IdentityModel> detail(int id) async => IdentityModel.fromJson(
    Map<String, dynamic>.from(
      (await dio.get('/api/v1/identity/detail/$id')).data,
    ),
  );
  Future<List<IdentityHistory>> history() async =>
      ((await dio.get('/api/v1/identity/history')).data['histories'] as List)
          .map((e) => IdentityHistory.fromJson(Map<String, dynamic>.from(e)))
          .toList();
}

final identityRepositoryProvider = Provider(
  (ref) => IdentityRepository(ref.watch(dioProvider).dio),
);
final identityProvider = FutureProvider.autoDispose(
  (ref) => ref.watch(identityRepositoryProvider).current(),
);
final identityDetailProvider = FutureProvider.autoDispose.family<IdentityModel, int>(
  (ref, id) => ref.watch(identityRepositoryProvider).detail(id),
);
final identityHistoryProvider = FutureProvider.autoDispose(
  (ref) => ref.watch(identityRepositoryProvider).history(),
);
