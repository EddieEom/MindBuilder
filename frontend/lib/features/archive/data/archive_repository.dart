import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../../app/app_provider.dart';

class ArchiveEvent {
  ArchiveEvent.fromJson(Map<String, dynamic> json)
    : id = json['event_id'] as int,
      referenceId = json['reference_id'] as int,
      type = json['event_type'] as String,
      title = json['title'] as String,
      summary = json['summary'] as String?,
      date = DateTime.parse(json['created_at'] as String);
  final int id, referenceId;
  final String type, title;
  final String? summary;
  final DateTime date;
}

class ArchiveRepository {
  ArchiveRepository(this.dio);
  final Dio dio;
  Future<Map<String, int>> summary() async => Map<String, dynamic>.from(
    (await dio.get('/api/v1/archive/summary')).data,
  ).map((k, v) => MapEntry(k, (v as num).toInt()));
  Future<List<ArchiveEvent>> events({
    int tab = 0,
    DateTime? date,
    String? type,
    int offset = 0,
  }) async {
    final path = tab == 1
        ? '/calendar'
        : tab == 2
        ? '/timeline'
        : tab == 3
        ? '/type/OS_UPDATED'
        : type == null
        ? '/recent'
        : '/type/${Uri.encodeComponent(type)}';
    final params = tab == 1
        ? <String, dynamic>{'date': DateFormat('yyyy-MM-dd').format(date!)}
        : <String, dynamic>{'limit': 30, 'offset': offset};
    return ((await dio.get(
              '/api/v1/archive$path',
              queryParameters: params,
            )).data['events']
            as List)
        .map((e) => ArchiveEvent.fromJson(Map<String, dynamic>.from(e)))
        .toList();
  }
}

final archiveRepositoryProvider = Provider(
  (ref) => ArchiveRepository(ref.watch(dioProvider).dio),
);
final archiveSummaryProvider = FutureProvider.autoDispose(
  (ref) => ref.watch(archiveRepositoryProvider).summary(),
);
