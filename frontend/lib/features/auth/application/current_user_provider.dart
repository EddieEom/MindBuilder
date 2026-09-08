import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/app_provider.dart';

import '../data/models/user_profile_model.dart';
import '../data/repositories/user_profile_repository.dart';

final userProfileRepositoryProvider = Provider<UserProfileRepository>((ref) {
  final dioClient = ref.watch(dioProvider);

  return UserProfileRepository(dioClient);
});

final currentUserProvider = FutureProvider.autoDispose<UserProfileModel>((
  ref,
) async {
  final repository = ref.watch(userProfileRepositoryProvider);

  return repository.getMe();
});
