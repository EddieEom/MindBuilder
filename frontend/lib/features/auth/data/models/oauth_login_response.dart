class OAuthLoginResponse {
  final String accessToken;
  final String refreshToken;
  final String tokenType;

  const OAuthLoginResponse({
    required this.accessToken,
    required this.refreshToken,
    required this.tokenType,
  });

  factory OAuthLoginResponse.fromJson(Map<String, dynamic> json) {
    return OAuthLoginResponse(
      accessToken: json['access_token'],
      refreshToken: json['refresh_token'],
      tokenType: json['token_type'],
    );
  }
}
