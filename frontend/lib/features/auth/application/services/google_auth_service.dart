import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:google_sign_in/google_sign_in.dart';

class GoogleUserData {
  final String email;
  final String nickname;
  final String providerUserId;
  final String profileImage;

  const GoogleUserData({
    required this.email,
    required this.nickname,
    required this.providerUserId,
    required this.profileImage,
  });
}

class GoogleAuthService {
  GoogleAuthService._();

  static final GoogleAuthService instance =
      GoogleAuthService._();

  final GoogleSignIn _googleSignIn =
      GoogleSignIn.instance;

  bool _initialized = false;

  Future<void> initialize() async {
    if (_initialized) return;

    final serverClientId =
        dotenv.env['GOOGLE_SERVER_CLIENT_ID'];

    if (serverClientId == null || serverClientId.isEmpty) {
      throw Exception(
        'GOOGLE_SERVER_CLIENT_ID가 .env에 설정되지 않았습니다.',
      );
    }

    await _googleSignIn.initialize(
      serverClientId: serverClientId,
    );

    _initialized = true;
  }

  Future<GoogleUserData?> signIn() async {
    await initialize();

    final GoogleSignInAccount account =
        await _googleSignIn.authenticate();

    return GoogleUserData(
      email: account.email,
      nickname: account.displayName ?? 'MindBuilder 사용자',
      providerUserId: account.id,
      profileImage: account.photoUrl ?? '',
    );
  }

  Future<void> signOut() async {
    await _googleSignIn.signOut();
  }
}