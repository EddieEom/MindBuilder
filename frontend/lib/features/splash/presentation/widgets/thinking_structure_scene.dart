import 'dart:async';

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

class ThinkingStructureScene extends StatefulWidget {
  final VoidCallback onComplete;

  const ThinkingStructureScene({
    super.key,
    required this.onComplete,
  });

  @override
  State<ThinkingStructureScene> createState() =>
      _ThinkingStructureSceneState();
}

class _ThinkingStructureSceneState
    extends State<ThinkingStructureScene>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 4500),
    )..forward();

    _controller.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        Timer(
          const Duration(milliseconds: 1400),
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
              child: CustomPaint(
                painter: _StructureBackgroundPainter(),
              ),
            ),

            Center(
              child: AnimatedBuilder(
                animation: _controller,
                builder: (context, child) {
                  return SizedBox(
                    width: 330,
                    height: 430,
                    child: CustomPaint(
                      painter: _ThinkingStructurePainter(
                        progress: _controller.value,
                      ),
                    ),
                  );
                },
              ),
            ),

            Center(
              child: FadeTransition(
                opacity: CurvedAnimation(
                  parent: _controller,
                  curve: const Interval(
                    0.35,
                    0.65,
                    curve: Curves.easeOut,
                  ),
                ),
                child: const Padding(
                  padding: EdgeInsets.symmetric(
                    horizontal: 36,
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        '당신만의',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.w700,
                          color: Color(0xFF252B3B),
                        ),
                      ),
                      SizedBox(height: 8),
                      Text(
                        '사고 구조와',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.w700,
                          color: AppColors.primary,
                        ),
                      ),
                      SizedBox(height: 8),
                      Text(
                        '성장 방식을',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.w700,
                          color: Color(0xFF252B3B),
                        ),
                      ),
                      SizedBox(height: 8),
                      Text(
                        '함께 발견합니다.',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.w700,
                          color: Color(0xFF252B3B),
                        ),
                      ),
                    ],
                  ),
                ),
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

  Widget _buildIndicator() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: List.generate(6, (index) {
        final active = index == 4;

        return Container(
          width: active ? 9 : 6,
          height: active ? 9 : 6,
          margin: const EdgeInsets.symmetric(
            horizontal: 5,
          ),
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

class _StructureBackgroundPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFFF1F2FF)
      ..style = PaintingStyle.fill;

    final path = Path()
      ..moveTo(0, size.height * 0.84)
      ..quadraticBezierTo(
        size.width * 0.2,
        size.height * 0.76,
        size.width * 0.45,
        size.height * 0.87,
      )
      ..quadraticBezierTo(
        size.width * 0.7,
        size.height * 0.97,
        size.width,
        size.height * 0.8,
      )
      ..lineTo(size.width, size.height)
      ..lineTo(0, size.height)
      ..close();

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(
    covariant _StructureBackgroundPainter oldDelegate,
  ) {
    return false;
  }
}

class _ThinkingStructurePainter extends CustomPainter {
  final double progress;

  _ThinkingStructurePainter({
    required this.progress,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final nodes = [
      Offset(size.width * 0.50, size.height * 0.18),
      Offset(size.width * 0.27, size.height * 0.30),
      Offset(size.width * 0.73, size.height * 0.30),
      Offset(size.width * 0.17, size.height * 0.50),
      Offset(size.width * 0.50, size.height * 0.48),
      Offset(size.width * 0.83, size.height * 0.50),
      Offset(size.width * 0.30, size.height * 0.70),
      Offset(size.width * 0.70, size.height * 0.70),
      Offset(size.width * 0.50, size.height * 0.84),
    ];

    final connections = [
      [0, 1],
      [0, 2],
      [1, 4],
      [2, 4],
      [1, 3],
      [2, 5],
      [3, 6],
      [4, 6],
      [4, 7],
      [5, 7],
      [6, 8],
      [7, 8],
    ];

    final lineProgress = Curves.easeOut.transform(
      ((progress - 0.05) / 0.55).clamp(0.0, 1.0),
    );

    final linePaint = Paint()
      ..color = AppColors.primary.withValues(alpha: 0.28)
      ..strokeWidth = 1.4
      ..style = PaintingStyle.stroke;

    for (final connection in connections) {
      final from = nodes[connection[0]];
      final to = nodes[connection[1]];

      final animatedEnd = Offset.lerp(
        from,
        to,
        lineProgress,
      )!;

      canvas.drawLine(
        from,
        animatedEnd,
        linePaint,
      );
    }

    for (int i = 0; i < nodes.length; i++) {
      final nodeProgress = Curves.easeOutBack.transform(
        ((progress - (i * 0.04)) / 0.35).clamp(0.0, 1.0),
      );

      if (nodeProgress <= 0) continue;

      final node = nodes[i];

      final radius = i == 4 ? 11.0 : 7.0;

      final glowPaint = Paint()
        ..color = AppColors.primary.withValues(
          alpha: 0.10 * nodeProgress,
        );

      final nodePaint = Paint()
        ..color = AppColors.primary.withValues(
          alpha: nodeProgress,
        );

      canvas.drawCircle(
        node,
        radius * 2.4,
        glowPaint,
      );

      canvas.drawCircle(
        node,
        radius * nodeProgress,
        nodePaint,
      );
    }

    final center = nodes[4];

    final centerGlow = Paint()
      ..color = AppColors.primary.withValues(alpha: 0.08);

    canvas.drawCircle(
      center,
      38,
      centerGlow,
    );
  }

  @override
  bool shouldRepaint(
    covariant _ThinkingStructurePainter oldDelegate,
  ) {
    return oldDelegate.progress != progress;
  }
}