import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../core/network/dio_client.dart';

final dioProvider = Provider<DioClient>((ref) {
  return DioClient();
});