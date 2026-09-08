class UserProfileModel {
  final String email;
  final String nickname;
  final String? profileImage;
  final String identityName;
  final String stage;
  final String provider;
  final int scanCount;
  final int patternCount;
  final int analysisCount;
  final int archiveCount;
  final int goalCount;

  const UserProfileModel({
    required this.email,
    required this.nickname,
    required this.profileImage,
    required this.identityName,
    required this.stage,
    required this.provider,
    required this.scanCount,
    required this.patternCount,
    required this.analysisCount,
    required this.archiveCount,
    required this.goalCount,
  });

  factory UserProfileModel.fromJson(Map<String, dynamic> json) {
    return UserProfileModel(
      email: json['email'] as String,
      nickname: json['nickname'] as String? ?? '사용자',
      profileImage: json['profile_image'] as String?,
      identityName: json['identity_name'] as String? ?? '',
      stage: json['stage'] as String? ?? '',
      provider: json['provider'] as String? ?? '',
      scanCount: (json['scan_count'] as num?)?.toInt() ?? 0,
      patternCount: (json['pattern_count'] as num?)?.toInt() ?? 0,
      analysisCount: (json['analysis_count'] as num?)?.toInt() ?? 0,
      archiveCount: (json['archive_count'] as num?)?.toInt() ?? 0,
      goalCount: (json['goal_count'] as num?)?.toInt() ?? 0,
    );
  }
}
