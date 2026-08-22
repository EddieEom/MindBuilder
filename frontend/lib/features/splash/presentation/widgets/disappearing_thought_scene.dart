import 'dart:async';

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

class DisappearingThoughtScene extends StatefulWidget {
  final VoidCallback onComplete;

  const DisappearingThoughtScene({
    super.key,
    required this.onComplete,
  });

  @override
  State<DisappearingThoughtScene> createState() =>
      _DisappearingThoughtSceneState();
}

class _DisappearingThoughtSceneState
    extends State<DisappearingThoughtScene> {
  final List<String> _thoughts = [
    '오늘 해야 할 일이 많은데',
    '이 선택이 맞을까?',
    '내일은 어떻게 될까?',
    '잘하고 있는 걸까?',
    '왜 이렇게 힘들지?',
  ];

  final List<bool> _visibleThoughts = List.generate(
    5,
    (_) => true,
  );

  @override
  void initState() {
    super.initState();
    _startDisappearAnimation();
  }

  Future<void> _startDisappearAnimation() async {
    await Future.delayed(const Duration(milliseconds: 700));

    for (int i = 0; i < _visibleThoughts.length; i++) {
      if (!mounted) return;

      setState(() {
        _visibleThoughts[i] = false;
      });

      await Future.delayed(
        const Duration(milliseconds: 600),
      );
    }

    await Future.delayed(
      const Duration(milliseconds: 800),
    );

    if (!mounted) return;

    widget.onComplete();
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
                painter: _ThoughtBackgroundPainter(),
              ),
            ),

            Center(
              child: Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 32,
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _buildThoughtCloud(),

                    const SizedBox(height: 40),

                    _buildText(),

                    const SizedBox(height: 40),

                    SizedBox(
                      height: 180,
                      width: double.infinity,
                      child: _buildThoughts(),
                    ),
                  ],
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

  Widget _buildThoughtCloud() {
    return AnimatedOpacity(
      duration: const Duration(milliseconds: 800),
      opacity: _visibleThoughts.any((value) => value) ? 1 : 0.25,
      child: Container(
        width: 130,
        height: 100,
        decoration: BoxDecoration(
          color: AppColors.primary.withValues(alpha: 0.08),
          borderRadius: BorderRadius.circular(48),
        ),
        child: const Icon(
          Icons.psychology_outlined,
          size: 58,
          color: AppColors.primary,
        ),
      ),
    );
  }

  Widget _buildText() {
    return const Column(
      children: [
        Text(
          '대부분의 생각은',
          textAlign: TextAlign.center,
          style: TextStyle(
            fontSize: 26,
            fontWeight: FontWeight.w700,
            color: Color(0xFF242B3D),
          ),
        ),
        SizedBox(height: 8),
        Text.rich(
          TextSpan(
            text: '기록되지 않은 채',
            style: TextStyle(
              fontSize: 26,
              fontWeight: FontWeight.w700,
              color: AppColors.primary,
            ),
          ),
          textAlign: TextAlign.center,
        ),
        SizedBox(height: 8),
        Text(
          '사라집니다.',
          textAlign: TextAlign.center,
          style: TextStyle(
            fontSize: 26,
            fontWeight: FontWeight.w700,
            color: Color(0xFF242B3D),
          ),
        ),
      ],
    );
  }

  Widget _buildThoughts() {
    return Stack(
      children: [
        _thoughtBubble(
          0,
          left: 10,
          top: 10,
        ),
        _thoughtBubble(
          1,
          right: 10,
          top: 35,
        ),
        _thoughtBubble(
          2,
          left: 60,
          top: 80,
        ),
        _thoughtBubble(
          3,
          right: 45,
          bottom: 20,
        ),
        _thoughtBubble(
          4,
          left: 20,
          bottom: 5,
        ),
      ],
    );
  }

  Widget _thoughtBubble(
    int index, {
    double? left,
    double? right,
    double? top,
    double? bottom,
  }) {
    return Positioned(
      left: left,
      right: right,
      top: top,
      bottom: bottom,
      child: AnimatedOpacity(
        duration: const Duration(milliseconds: 500),
        opacity: _visibleThoughts[index] ? 1 : 0,
        child: AnimatedScale(
          duration: const Duration(milliseconds: 500),
          scale: _visibleThoughts[index] ? 1 : 0.7,
          child: Container(
            padding: const EdgeInsets.symmetric(
              horizontal: 14,
              vertical: 9,
            ),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(
                color: const Color(0xFFE2E5F4),
              ),
            ),
            child: Text(
              _thoughts[index],
              style: const TextStyle(
                fontSize: 12,
                color: Color(0xFF666D80),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildIndicator() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: List.generate(5, (index) {
        final active = index == 1;

        return Container(
          width: active ? 8 : 6,
          height: active ? 8 : 6,
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

class _ThoughtBackgroundPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFFF2F3FF)
      ..style = PaintingStyle.fill;

    final path = Path()
      ..moveTo(0, size.height * 0.82)
      ..quadraticBezierTo(
        size.width * 0.25,
        size.height * 0.75,
        size.width * 0.5,
        size.height * 0.88,
      )
      ..quadraticBezierTo(
        size.width * 0.75,
        size.height * 0.98,
        size.width,
        size.height * 0.8,
      )
      ..lineTo(size.width, size.height)
      ..lineTo(0, size.height)
      ..close();

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return false;
  }
}