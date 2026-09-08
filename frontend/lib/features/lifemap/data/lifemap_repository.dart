import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../app/app_provider.dart';

class MapGoal {
  MapGoal.fromJson(Map<String, dynamic> json)
    : title = json['title'] as String,
      progress = (json['progress'] as num).toDouble(),
      status = json['status'] as String;
  final String title;
  final double progress;
  final String status;
}

class MapNode {
  MapNode.fromJson(Map<String, dynamic> json)
    : id = json['node_id'].toString(),
      title = json['title'] as String,
      type = json['node_type'] as String,
      importance = (json['importance'] as num).toDouble(),
      color = json['color'] as String,
      summary = json['summary'] as String? ?? '',
      x = (json['x'] as num).toDouble(),
      y = (json['y'] as num).toDouble(),
      tags = (json['tags'] as List).map((e) => e['name'] as String).toList(),
      goals = (json['related_goals'] as List)
          .map((e) => MapGoal.fromJson(Map<String, dynamic>.from(e)))
          .toList();
  final String id, title, type, color, summary;
  final double importance, x, y;
  final List<String> tags;
  final List<MapGoal> goals;
}

class MapEdge {
  MapEdge.fromJson(Map<String, dynamic> json)
    : from = json['from_node'].toString(),
      to = json['to_node'].toString();
  final String from, to;
}

class LifeMapModel {
  LifeMapModel.fromJson(Map<String, dynamic> json)
    : title = json['title'] as String,
      nodes = (json['nodes'] as List)
          .map((e) => MapNode.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      edges = (json['edges'] as List)
          .map((e) => MapEdge.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      overview = Map<String, dynamic>.from(json['overview']),
      metadata = Map<String, dynamic>.from(json['metadata']);
  final String title;
  final List<MapNode> nodes;
  final List<MapEdge> edges;
  final Map<String, dynamic> overview, metadata;
}

class LifeMapRepository {
  LifeMapRepository(this.dio);
  final Dio dio;
  Future<LifeMapModel> current() async => LifeMapModel.fromJson(
    Map<String, dynamic>.from((await dio.get('/api/v1/lifemap')).data),
  );
  Future<List<LifeMapModel>> history() async =>
      ((await dio.get('/api/v1/lifemap/history')).data as List)
          .map((e) => LifeMapModel.fromJson(Map<String, dynamic>.from(e)))
          .toList();
  Future<MapNode> node(String id) async => MapNode.fromJson(
    Map<String, dynamic>.from(
      (await dio.get('/api/v1/lifemap/node/${Uri.encodeComponent(id)}')).data,
    ),
  );
}

final lifeMapRepositoryProvider = Provider(
  (ref) => LifeMapRepository(ref.watch(dioProvider).dio),
);
final lifeMapProvider = FutureProvider.autoDispose(
  (ref) => ref.watch(lifeMapRepositoryProvider).current(),
);
final lifeMapHistoryProvider = FutureProvider.autoDispose(
  (ref) => ref.watch(lifeMapRepositoryProvider).history(),
);
final lifeMapNodeProvider = FutureProvider.autoDispose.family<MapNode, String>(
  (ref, id) => ref.watch(lifeMapRepositoryProvider).node(id),
);
