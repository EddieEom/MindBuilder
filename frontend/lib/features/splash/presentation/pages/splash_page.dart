import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../widgets/connected_nodes_scene.dart';
import '../widgets/disappearing_thought_scene.dart';
import '../widgets/final_growth_scene.dart';
import '../widgets/scattered_thought_scene.dart';
import '../widgets/splash_logo_scene.dart';
import '../widgets/thinking_structure_scene.dart';
import '../widgets/thought_bubble_scene.dart';
import '../../../../core/storage/token_storage.dart';
import '../../../../core/network/dio_client.dart';

class SplashPage extends StatefulWidget {
  const SplashPage({super.key});

  @override
  State<SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends State<SplashPage> {
  int _sceneIndex = 0;

  void _nextScene() {
    if (!mounted) return;

    setState(() {
      _sceneIndex++;
    });
  }

  Future<void> _handleSplashComplete() async {
    final accessToken = await TokenStorage.instance.getAccessToken();

    if (!mounted) return;

    if (accessToken != null && accessToken.isNotEmpty) {
      try {
        await DioClient().dio.get('/auth/me');
        if (mounted) context.go('/dashboard');
      } catch (_) {
        await TokenStorage.instance.clearTokens();
        if (mounted) context.go('/login');
      }
    } else {
      context.go('/login');
    }
  }

  @override
  Widget build(BuildContext context) {
    Widget scene;

    switch (_sceneIndex) {
      case 0:
        scene = SplashLogoScene(
          key: const ValueKey('logo'),
          onComplete: _nextScene,
        );

      case 1:
        scene = ThoughtBubbleScene(
          key: const ValueKey('thought'),
          onComplete: _nextScene,
        );

      case 2:
        scene = DisappearingThoughtScene(
          key: const ValueKey('disappear'),
          onComplete: _nextScene,
        );

      case 3:
        scene = ScatteredThoughtScene(
          key: const ValueKey('scattered'),
          onComplete: _nextScene,
        );

      case 4:
        scene = ConnectedNodesScene(
          key: const ValueKey('connected'),
          onComplete: _nextScene,
        );

      case 5:
        scene = ThinkingStructureScene(
          key: const ValueKey('thinking_structure'),
          onComplete: _nextScene,
        );

      case 6:
        scene = FinalGrowthScene(
          key: const ValueKey('final_growth'),
          onComplete: _handleSplashComplete,
        );

      default:
        scene = const SizedBox.shrink();
    }

    return Scaffold(
      body: Stack(
        children: [
          AnimatedSwitcher(
            duration: const Duration(milliseconds: 700),
            switchInCurve: Curves.easeOut,
            switchOutCurve: Curves.easeIn,
            child: scene,
          ),

          SafeArea(
            child: Align(
              alignment: Alignment.topRight,
              child: Padding(
                padding: const EdgeInsets.only(top: 12, right: 20),
                child: TextButton(
                  onPressed: _handleSplashComplete,
                  style: TextButton.styleFrom(
                    foregroundColor: Colors.black54,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 8,
                    ),
                  ),
                  child: const Text(
                    '건너뛰기',
                    style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
