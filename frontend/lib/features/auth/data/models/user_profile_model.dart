class UserProfileModel {
  final int userId;
  final String email;
  final String nickname;
  final String? profileImage;

  const UserProfileModel({
    required this.userId,
    required this.email,
    required this.nickname,
    required this.profileImage,
  });

  factory UserProfileModel.fromJson(
    Map<String, dynamic> json,
  ) {
    return UserProfileModel(
      userId: json['user_id'] as int,
      email: json['email'] as String,
      nickname: json['nickname'] as String? ?? '사용자',
      profileImage: json['profile_image'] as String?,
    );
  }
}