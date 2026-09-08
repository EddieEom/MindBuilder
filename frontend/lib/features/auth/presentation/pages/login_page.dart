import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import '../../../../core/theme/app_colors.dart';
import 'package:go_router/go_router.dart';
import '../../data/repositories/auth_repository.dart';
import '../../application/services/google_auth_service.dart';
import '../../../../core/storage/token_storage.dart';
import '../../../../core/routes/route_names.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  bool _isLoading = false;

  Future<void> _handleGoogleLogin() async {
    if (_isLoading) return;

    setState(() {
      _isLoading = true;
    });

    try {
      // 1. Google 로그인
      final googleUser = await GoogleAuthService.instance.signIn();

      if (googleUser == null) {
        return;
      }

      // 2. 백엔드 OAuth 로그인
      final authRepository = AuthRepository();

      final result = await authRepository.loginWithOAuth(
        email: googleUser.email,
        nickname: googleUser.nickname,
        provider: 'google',
        providerUserId: googleUser.providerUserId,
        profileImage: googleUser.profileImage,
      );

      final accessToken = result['access_token'] as String;

      final refreshToken = result['refresh_token'] as String;

      await TokenStorage.instance.saveTokens(
        accessToken: accessToken,
        refreshToken: refreshToken,
      );

      if (!mounted) return;
      final isNewUser = result['is_new_user'] as bool? ?? false;
      context.go(isNewUser ? RouteNames.onboarding : RouteNames.dashboard);
    } on DioException catch (e) {
      debugPrint('===== LOGIN ERROR =====');

      debugPrint('Status Code: ${e.response?.statusCode}');

      debugPrint('Response Data: ${e.response?.data}');

      debugPrint('Request Data: ${e.requestOptions.data}');

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('로그인 요청에 실패했습니다. (${e.response?.statusCode})')),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('로그인을 완료하지 못했습니다. 다시 시도해 주세요.')),
      );
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Column(
            children: [
              const Spacer(flex: 2),

              // Logo
              Container(
                width: 64,
                height: 64,
                decoration: BoxDecoration(
                  color: AppColors.primary.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Icon(
                  Icons.psychology_alt_outlined,
                  size: 34,
                  color: AppColors.primary,
                ),
              ),

              const SizedBox(height: 16),

              Text(
                'Mind Builder',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: AppColors.primary,
                ),
              ),

              const SizedBox(height: 6),

              Text(
                'AI 시대의 인간 운영체제 시스템',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),

              const SizedBox(height: 32),

              Divider(color: AppColors.border),

              const SizedBox(height: 28),

              RichText(
                textAlign: TextAlign.center,
                text: TextSpan(
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    height: 1.55,
                    fontWeight: FontWeight.w600,
                    color: AppColors.textPrimary,
                  ),
                  children: [
                    const TextSpan(text: '당신의 '),
                    TextSpan(
                      text: '생각',
                      style: TextStyle(
                        color: AppColors.primary,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const TextSpan(text: '은\n인생의 데이터가 되고\n성장이 됩니다.'),
                  ],
                ),
              ),

              const SizedBox(height: 36),

              _SocialLoginButton(
                icon: const Text(
                  'G',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                text: _isLoading ? '로그인 중...' : 'Google로 계속하기',
                onPressed: _isLoading ? () {} : _handleGoogleLogin,
              ),

              const SizedBox(height: 12),

              _SocialLoginButton(
                icon: Container(
                  width: 26,
                  height: 26,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    color: const Color(0xFFFFE812),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: const Icon(
                    Icons.chat_bubble,
                    size: 16,
                    color: Colors.black87,
                  ),
                ),
                text: 'Kakao로 계속하기',
                onPressed: () {
                  // STEP 3에서 Kakao Login 연결
                },
              ),

              const Spacer(flex: 2),

              Divider(color: AppColors.border),

              const SizedBox(height: 16),

              Text(
                '오늘도 누군가는 자신의 사고 구조를 발견하고 있습니다.',
                textAlign: TextAlign.center,
                style: Theme.of(
                  context,
                ).textTheme.bodySmall?.copyWith(color: AppColors.textSecondary),
              ),

              const SizedBox(height: 6),

              Text(
                '당신의 사고 데이터는 오직 당신만을 위해 저장됩니다.',
                textAlign: TextAlign.center,
                style: Theme.of(
                  context,
                ).textTheme.bodySmall?.copyWith(color: AppColors.textSecondary),
              ),

              const SizedBox(height: 16),

              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  TextButton(onPressed: () {}, child: const Text('개인정보처리방침')),
                  const Text('·'),
                  TextButton(onPressed: () {}, child: const Text('이용약관')),
                ],
              ),

              const SizedBox(height: 12),
            ],
          ),
        ),
      ),
    );
  }
}

class _SocialLoginButton extends StatelessWidget {
  const _SocialLoginButton({
    required this.icon,
    required this.text,
    required this.onPressed,
  });

  final Widget icon;
  final String text;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 56,
      child: OutlinedButton(
        onPressed: onPressed,
        style: OutlinedButton.styleFrom(
          backgroundColor: Colors.white,
          foregroundColor: AppColors.textPrimary,
          side: BorderSide(color: AppColors.border),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
        child: Stack(
          alignment: Alignment.center,
          children: [
            Align(alignment: Alignment.centerLeft, child: icon),
            Text(
              text,
              style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
            ),
          ],
        ),
      ),
    );
  }
}
