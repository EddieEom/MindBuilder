import 'package:go_router/go_router.dart';

import '../../features/auth/presentation/pages/login_page.dart';
import '../../features/dashboard/presentation/pages/dashboard_page.dart';
import '../../features/onboarding/presentation/pages/onboarding_page.dart';
import '../../features/onboarding/presentation/pages/onboarding_intro_page.dart';
import '../../features/splash/presentation/pages/splash_page.dart';

import 'route_names.dart';

abstract final class AppRouter {
  static GoRouter createRouter({
    required bool isLoggedIn,
  }) {
    return GoRouter(
      initialLocation: isLoggedIn
          ? RouteNames.dashboard
          : RouteNames.splash,

      routes: [
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
          builder: (context, state) =>
              const OnboardingIntroPage(),
        ),

        // 첫 Scan
        GoRoute(
          path: RouteNames.scan,
          builder: (context, state) =>
              const OnboardingPage(),
        ),

        GoRoute(
          path: RouteNames.dashboard,
          builder: (context, state) =>
              const DashboardPage(),
        ),
      ],
    );
  }
}