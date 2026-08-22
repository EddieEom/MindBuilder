import 'dart:async';
import 'dart:math';

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

class FinalGrowthScene extends StatefulWidget {
  final VoidCallback onComplete;

  const FinalGrowthScene({
    super.key,
    required this.onComplete,
  });

  @override
  State<FinalGrowthScene> createState() => _FinalGrowthSceneState();
}

class _FinalGrowthSceneState extends State<FinalGrowthScene>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 5200),
    )..forward();

    _controller.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        Timer(
          const Duration(milliseconds: 1800),
          () {
            if (mounted) {
              widget.onComplete();
            }
          },
        );
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF9FAFF),
      body: SafeArea(
        child: Stack(
          children: [
            Positioned.fill(
              child: AnimatedBuilder(
                animation: _controller,
                builder: (context, child) {
                  return CustomPaint(
                    painter: _FinalSceneBackgroundPainter(
                      progress: _controller.value,
                    ),
                  );
                },
              ),
            ),

            Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  SizedBox(
                    width: 320,
                    height: 400,
                    child: AnimatedBuilder(
                      animation: _controller,
                      builder: (context, child) {
                        return CustomPaint(
                          painter: _GrowthPlantPainter(
                            progress: _controller.value,
                          ),
                        );
                      },
                    ),
                  ),

                  const SizedBox(height: 8),

                  _buildMessage(),
                ],
              ),
            ),

            Positioned(
              left: 0,
              right: 0,
              bottom: 36,
              child: _buildIndicator(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMessage() {
    final fadeAnimation = CurvedAnimation(
      parent: _controller,
      curve: const Interval(
        0.52,
        0.82,
        curve: Curves.easeOut,
      ),
    );

    return FadeTransition(
      opacity: fadeAnimation,
      child: SlideTransition(
        position: Tween<Offset>(
          begin: const Offset(0, 0.12),
          end: Offset.zero,
        ).animate(
          CurvedAnimation(
            parent: _controller,
            curve: const Interval(
              0.52,
              0.82,
              curve: Curves.easeOut,
            ),
          ),
        ),
        child: const Column(
          children: [
            Text(
              '지금부터',
              style: TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.w700,
                color: Color(0xFF252B3B),
              ),
            ),

            SizedBox(height: 8),

            Text(
              '당신만의',
              style: TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.w700,
                color: Color(0xFF252B3B),
              ),
            ),

            SizedBox(height: 8),

            Text(
              '인간 운영체제를',
              style: TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.w700,
                color: AppColors.primary,
              ),
            ),

            SizedBox(height: 8),

            Text(
              '만들어드리겠습니다.',
              style: TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.w700,
                color: Color(0xFF252B3B),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildIndicator() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: List.generate(5, (index) {
        final active = index == 4;

        return Container(
          width: active ? 10 : 7,
          height: active ? 10 : 7,
          margin: const EdgeInsets.symmetric(horizontal: 7),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: active
                ? AppColors.primary
                : const Color(0xFFD9DCE7),
          ),
        );
      }),
    );
  }
}

class _FinalSceneBackgroundPainter extends CustomPainter {
  final double progress;

  _FinalSceneBackgroundPainter({
    required this.progress,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final random = Random(10);

    final particleProgress =
        ((progress - 0.15) / 0.55).clamp(0.0, 1.0);

    for (int i = 0; i < 22; i++) {
      final x = random.nextDouble() * size.width;
      final y = random.nextDouble() * size.height * 0.58;

      final opacity =
          random.nextDouble() * 0.35 * particleProgress;

      final paint = Paint()
        ..color = AppColors.primary.withValues(
          alpha: opacity,
        );

      canvas.drawCircle(
        Offset(x, y),
        random.nextDouble() * 2 + 1,
        paint,
      );
    }

    final groundOpacity =
        ((progress - 0.05) / 0.35).clamp(0.0, 1.0);

    final glowPaint = Paint()
      ..color = AppColors.primary.withValues(
        alpha: 0.10 * groundOpacity,
      );

    final center = Offset(
      size.width / 2,
      size.height * 0.43,
    );

    canvas.drawOval(
      Rect.fromCenter(
        center: center,
        width: 280,
        height: 90,
      ),
      glowPaint,
    );

    final ringPaint = Paint()
      ..color = AppColors.primary.withValues(
        alpha: 0.10 * groundOpacity,
      )
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1;

    canvas.drawOval(
      Rect.fromCenter(
        center: center,
        width: 330,
        height: 110,
      ),
      ringPaint,
    );
  }

  @override
  bool shouldRepaint(
    covariant _FinalSceneBackgroundPainter oldDelegate,
  ) {
    return oldDelegate.progress != progress;
  }
}

class _GrowthPlantPainter extends CustomPainter {
  final double progress;

  _GrowthPlantPainter({
    required this.progress,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final baseX = size.width / 2;
    final baseY = size.height * 0.78;

    final growthProgress =
        Curves.easeOutCubic.transform(
      ((progress - 0.08) / 0.55).clamp(0.0, 1.0),
    );

    // 씨앗이 놓인 지면
    final soilOpacity =
        ((progress - 0.05) / 0.25).clamp(0.0, 1.0);

    final soilPaint = Paint()
      ..color = AppColors.primary.withValues(
        alpha: 0.45 * soilOpacity,
      );

    final soilPath = Path()
      ..moveTo(baseX - 42, baseY)
      ..quadraticBezierTo(
        baseX,
        baseY - 16,
        baseX + 42,
        baseY,
      )
      ..quadraticBezierTo(
        baseX,
        baseY + 10,
        baseX - 42,
        baseY,
      )
      ..close();

    canvas.drawPath(soilPath, soilPaint);

    // 줄기 성장
    final stemHeight = 120 * growthProgress;

    final stemPaint = Paint()
      ..color = const Color(0xFF58A65C)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 5
      ..strokeCap = StrokeCap.round;

    final stemPath = Path()
      ..moveTo(baseX, baseY - 3)
      ..quadraticBezierTo(
        baseX - 2,
        baseY - stemHeight * 0.55,
        baseX,
        baseY - stemHeight,
      );

    final metric = stemPath.computeMetrics().first;

    final visibleStem = metric.extractPath(
      0,
      metric.length * growthProgress,
    );

    canvas.drawPath(
      visibleStem,
      stemPaint,
    );

    // 왼쪽 잎
    final leftLeafProgress =
        ((progress - 0.35) / 0.30).clamp(0.0, 1.0);

    if (leftLeafProgress > 0) {
      final leafScale =
          Curves.easeOutBack.transform(leftLeafProgress);

      canvas.save();

      canvas.translate(
        baseX - 2,
        baseY - stemHeight * 0.55,
      );

      canvas.scale(leafScale);

      final leftLeaf = Path()
        ..moveTo(0, 0)
        ..quadraticBezierTo(
          -45,
          -15,
          -55,
          -50,
        )
        ..quadraticBezierTo(
          -12,
          -52,
          0,
          0,
        )
        ..close();

      final leftLeafPaint = Paint()
        ..shader = const LinearGradient(
          colors: [
            Color(0xFF74B968),
            Color(0xFFA9D97A),
          ],
        ).createShader(
          const Rect.fromLTWH(
            -60,
            -60,
            70,
            70,
          ),
        );

      canvas.drawPath(leftLeaf, leftLeafPaint);

      canvas.restore();
    }

    // 오른쪽 잎
    final rightLeafProgress =
        ((progress - 0.45) / 0.32).clamp(0.0, 1.0);

    if (rightLeafProgress > 0) {
      final leafScale =
          Curves.easeOutBack.transform(rightLeafProgress);

      canvas.save();

      canvas.translate(
        baseX,
        baseY - stemHeight * 0.88,
      );

      canvas.scale(leafScale);

      final rightLeaf = Path()
        ..moveTo(0, 0)
        ..quadraticBezierTo(
          42,
          -8,
          55,
          -55,
        )
        ..quadraticBezierTo(
          12,
          -58,
          0,
          0,
        )
        ..close();

      final rightLeafPaint = Paint()
        ..shader = const LinearGradient(
          colors: [
            Color(0xFF7FBE68),
            Color(0xFFC3E789),
          ],
        ).createShader(
          const Rect.fromLTWH(
            0,
            -70,
            70,
            70,
          ),
        );

      canvas.drawPath(
        rightLeaf,
        rightLeafPaint,
      );

      canvas.restore();
    }
  }

  @override
  bool shouldRepaint(
    covariant _GrowthPlantPainter oldDelegate,
  ) {
    return oldDelegate.progress != progress;
  }
}