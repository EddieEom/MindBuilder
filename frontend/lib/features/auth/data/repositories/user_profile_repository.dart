import '../../../../core/network/dio_client.dart';
import 'dart:convert';
import 'dart:typed_data';

import 'package:dio/dio.dart';

import '../models/user_profile_model.dart';

class UserProfileRepository {
  final DioClient _dioClient;

  UserProfileRepository(this._dioClient);

  Future<UserProfileModel> getMe() async {
    final response = await _dioClient.dio.get('/auth/me');

    return UserProfileModel.fromJson(response.data as Map<String, dynamic>);
  }

  Future<String> updateNickname(String nickname) async {
    final response = await _dioClient.dio.patch(
      '/auth/me',
      data: {'nickname': nickname},
    );
    return response.data['nickname'] as String;
  }

  Future<String> updateProfileImage(String imageUrl) async {
    final response = await _dioClient.dio.patch(
      '/auth/profile-image',
      data: {'profile_image': imageUrl},
    );
    return response.data['profile_image'] as String;
  }

  Future<String> exportData() async {
    final response = await _dioClient.dio.get('/auth/export');
    return const JsonEncoder.withIndent('  ').convert(response.data);
  }

  Future<Uint8List> exportPdf() async {
    final response = await _dioClient.dio.get<List<int>>(
      '/auth/export/pdf',
      options: Options(responseType: ResponseType.bytes),
    );
    return Uint8List.fromList(response.data!);
  }

  Future<void> deleteAccount() async {
    await _dioClient.dio.delete('/auth/me');
  }
}
