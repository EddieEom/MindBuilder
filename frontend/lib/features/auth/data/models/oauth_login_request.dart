class OAuthLoginRequest {
  final String email;
  final String nickname;
  final String providerUserId;
  final String profileImage;

  const OAuthLoginRequest({
    required this.email,
    required this.nickname,
    required this.providerUserId,
    required this.profileImage,
  });

  Map<String, dynamic> toJson() {
    return {
      'email': email,
      'nickname': nickname,
      'provider_user_id': providerUserId,
      'profile_image': profileImage,
    };
  }
}
