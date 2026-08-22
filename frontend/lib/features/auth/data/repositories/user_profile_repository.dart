import '../../../../core/network/dio_client.dart';

import '../models/user_profile_model.dart';

class UserProfileRepository {
  final DioClient _dioClient;

  UserProfileRepository(this._dioClient);

  Future<UserProfileModel> getMe() async {
    final response = await _dioClient.dio.get(
      '/auth/me',
    );

    return UserProfileModel.fromJson(
      response.data as Map<String, dynamic>,
    );
  }
}