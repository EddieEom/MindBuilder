import 'package:go_router/go_router.dart';

import '../../features/auth/presentation/pages/login_page.dart';
import '../../features/dashboard/presentation/pages/dashboard_page.dart';
import '../../features/onboarding/presentation/pages/onboarding_page.dart';
import '../../features/onboarding/presentation/pages/onboarding_intro_page.dart';
import '../../features/splash/presentation/pages/splash_page.dart';
import '../../features/analysis/presentation/pages/analysis_loading_page.dart';
import '../../features/growth/presentation/pages/growth_page.dart';
import '../../features/lifemap/presentation/lifemap_page.dart';
import '../../features/identity/presentation/identity_page.dart';
import '../../features/hos/presentation/hos_page.dart';
import '../../features/archive/presentation/archive_page.dart';
import '../../features/profile/presentation/profile_page.dart';
import '../../features/settings/presentation/settings_page.dart';

import 'route_names.dart';

abstract final class AppRouter {
  static GoRouter createRouter({required bool isLoggedIn}) {
    return GoRouter(
      initialLocation: isLoggedIn ? RouteNames.dashboard : RouteNames.splash,

      routes: [
        GoRoute(
          path: RouteNames.profile,
          builder: (context, state) => const ProfilePage(),
        ),
        GoRoute(
          path: RouteNames.settings,
          builder: (context, state) => const SettingsPage(),
        ),
        GoRoute(
          path: RouteNames.archive,
          builder: (context, state) => const ArchivePage(),
        ),
        GoRoute(
          path: RouteNames.hos,
          builder: (context, state) => const HosPage(),
        ),
        GoRoute(
          path: RouteNames.identity,
          builder: (context, state) => const IdentityPage(),
        ),
        GoRoute(
          path: '/identity/:identityId',
          builder: (context, state) => IdentityPage(
            identityId: int.parse(state.pathParameters['identityId']!),
          ),
        ),
        GoRoute(
          path: RouteNames.lifemap,
          builder: (context, state) => const LifeMapPage(),
        ),
        GoRoute(
          path: '/lifemap/node/:nodeId',
          builder: (context, state) =>
              LifeMapNodePage(nodeId: state.pathParameters['nodeId']!),
        ),
        GoRoute(
          path: RouteNames.splash,
          builder: (context, state) => const SplashPage(),
        ),

        GoRoute(
          path: RouteNames.login,
          builder: (context, state) => const LoginPage(),
        ),

        // 온보딩 Intro
        GoRoute(
          path: RouteNames.onboarding,
          builder: (context, state) => const OnboardingIntroPage(),
        ),

        GoRoute(
          path: RouteNames.analysis,
          builder: (context, state) {
            final extra = state.extra as Map<String, dynamic>;

            return AnalysisLoadingPage(
              scanId: extra['scanId'],
              analysisResult: extra['analysisResult'],
            );
          },
        ),

        // 첫 Scan
        GoRoute(
          path: RouteNames.scan,
          builder: (context, state) => const OnboardingPage(),
        ),

        GoRoute(
          path: RouteNames.dashboard,
          builder: (context, state) {
            final extra = state.extra as Map?;

            return DashboardPage(refresh: extra?['refresh'] ?? false);
          },
        ),

        GoRoute(
          path: RouteNames.growth,
          builder: (context, state) => const GrowthPage(),
        ),
      ],
    );
  }
}
