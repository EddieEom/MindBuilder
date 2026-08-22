import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

class SplashLogoScene extends StatefulWidget {
  final VoidCallback onComplete;

  const SplashLogoScene({
    super.key,
    required this.onComplete,
  });

  @override
  State<SplashLogoScene> createState() => _SplashLogoSceneState();
}

class _SplashLogoSceneState extends State<SplashLogoScene>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  late final Animation<double> _logoOpacity;
  late final Animation<double> _logoScale;
  late final Animation<double> _progress;

  @override
  void initState() {
  super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2800),
    );

    _controller.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        Future.delayed(
          const Duration(milliseconds: 300),
          () {
            if (mounted) {
              widget.onComplete();
            }
          },
        );
      }
    });

    _logoOpacity = CurvedAnimation(
      parent: _controller,
      curve: const Interval(
        0.0,
        0.35,
        curve: Curves.easeOut,
      ),
    );

    _logoScale = Tween<double>(
      begin: 0.85,
      end: 1.0,
    ).animate(
      CurvedAnimation(
        parent: _controller,
        curve: const Interval(
          0.0,
          0.4,
          curve: Curves.easeOutBack,
        ),
      ),
    );

    _progress = CurvedAnimation(
      parent: _controller,
      curve: const Interval(
        0.25,
        1.0,
        curve: Curves.easeInOut,
      ),
    );

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FF),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(28),
          child: Column(
            children: [
              Expanded(
                child: Center(
                  child: FadeTransition(
                    opacity: _logoOpacity,
                    child: ScaleTransition(
                      scale: _logoScale,
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          _buildBrainLogo(),

                          const SizedBox(height: 28),

                          const Text(
                            'Mind Builder',
                            style: TextStyle(
                              fontSize: 34,
                              fontWeight: FontWeight.w700,
                              color: Color(0xFF3F4FA5),
                              letterSpacing: -1.2,
                            ),
                          ),

                          const SizedBox(height: 10),

                          const Text(
                            'AI Human Operating System',
                            style: TextStyle(
                              fontSize: 18,
                              color: Color(0xFF5D6478),
                              letterSpacing: -0.2,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),

              AnimatedBuilder(
                animation: _controller,
                builder: (context, child) {
                  return Column(
                    children: [
                      ClipRRect(
                        borderRadius: BorderRadius.circular(10),
                        child: LinearProgressIndicator(
                          value: _progress.value,
                          minHeight: 4,
                          backgroundColor: const Color(0xFFE2E5F5),
                          valueColor:
                              const AlwaysStoppedAnimation<Color>(
                            AppColors.primary,
                          ),
                        ),
                      ),

                      const SizedBox(height: 24),

                      FadeTransition(
                        opacity: _progress,
                        child: const Text(
                          'Loading...',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w500,
                            color: Color(0xFF5C5BB0),
                          ),
                        ),
                      ),
                    ],
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildBrainLogo() {
    return Container(
      width: 92,
      height: 92,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: const Color(0xFFEEEFFF),
        boxShadow: [
          BoxShadow(
            color: AppColors.primary.withValues(alpha: 0.12),
            blurRadius: 30,
            spreadRadius: 5,
          ),
        ],
      ),
      child: const Icon(
        Icons.psychology_outlined,
        size: 50,
        color: AppColors.primary,
      ),
    );
  }
}