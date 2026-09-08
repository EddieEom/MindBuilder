import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../app/app_provider.dart';

class HosValue {
  HosValue.fromJson(Map<String, dynamic> json)
    : name = json['value_name'] as String,
      description = json['description'] as String?;
  final String name;
  final String? description;
}

class HosModel {
  HosModel.fromJson(Map<String, dynamic> json)
    : id = json['os_id'] as int,
      version = json['version'] as String,
      stage = json['stage'] as String,
      confidence = (json['confidence_score'] as num?)?.toDouble(),
      confidenceLabel = json['data_confidence'] as String,
      values = (json['core_values'] as List)
          .map((e) => HosValue.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      thinking = json['thinking_pattern'] as String,
      decision = json['decision_pattern'] as String,
      rules = List<String>.from(json['operating_rules']),
      metadata = Map<String, dynamic>.from(json['metadata'] ?? {}),
      scores = Map<String, dynamic>.from(
        json['pattern_scores'] ?? {},
      ).map((k, v) => MapEntry(k, (v as num).toDouble()));
  final int id;
  final String version, stage, confidenceLabel, thinking, decision;
  final double? confidence;
  final List<HosValue> values;
  final List<String> rules;
  final Map<String, dynamic> metadata;
  final Map<String, double> scores;
}

class HosVersion {
  HosVersion.fromJson(Map<String, dynamic> json)
    : id = json['os_id'] as int,
      version = json['version'] as String,
      stage = json['stage'] as String,
      date = DateTime.parse(json['generated_at'] as String),
      current = json['is_current'] as bool;
  final int id;
  final String version, stage;
  final DateTime date;
  final bool current;
}

class HosRepository {
  HosRepository(this.dio);
  final Dio dio;
  Future<HosModel> current() async => HosModel.fromJson(
    Map<String, dynamic>.from(
      (await dio.get('/api/v1/operating-system/current')).data,
    ),
  );
  Future<List<HosModel>> history() async =>
      ((await dio.get('/api/v1/operating-system/history')).data as List)
          .map((e) => HosModel.fromJson(Map<String, dynamic>.from(e)))
          .toList();
  Future<List<HosVersion>> versions() async =>
      ((await dio.get('/api/v1/operating-system/version')).data as List)
          .map((e) => HosVersion.fromJson(Map<String, dynamic>.from(e)))
          .toList();
}

final hosRepositoryProvider = Provider(
  (ref) => HosRepository(ref.watch(dioProvider).dio),
);
final hosProvider = FutureProvider.autoDispose(
  (ref) => ref.watch(hosRepositoryProvider).current(),
);
final hosHistoryProvider = FutureProvider.autoDispose(
  (ref) => ref.watch(hosRepositoryProvider).history(),
);
final hosVersionsProvider = FutureProvider.autoDispose(
  (ref) => ref.watch(hosRepositoryProvider).versions(),
);
