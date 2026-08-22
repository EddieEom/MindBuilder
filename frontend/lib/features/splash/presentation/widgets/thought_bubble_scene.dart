import 'dart:async';

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

class ThoughtBubbleScene extends StatefulWidget {
  final VoidCallback onComplete;

  const ThoughtBubbleScene({
    super.key,
    required this.onComplete,
  });

  @override
  State<ThoughtBubbleScene> createState() =>
      _ThoughtBubbleSceneState();
}

class _ThoughtBubbleSceneState
    extends State<ThoughtBubbleScene>
    with TickerProviderStateMixin {
  final List<String> _thoughts = [
    '오늘 해야 할 일이 많은데',
    '이 선택이 맞을까?',
    '내일은 어떻게 될까?',
  ];

  int _visibleThoughtCount = 0;

  Timer? _timer;

  @override
  void initState() {
    super.initState();

    _startThoughtAnimation();
  }

  void _startThoughtAnimation() {
    _timer = Timer.periodic(
      const Duration(milliseconds: 700),
      (timer) {
        if (_visibleThoughtCount >= _thoughts.length) {
            timer.cancel();

            Future.delayed(
                const Duration(milliseconds: 1200),
                () {
                if (mounted) {
                    widget.onComplete();
                }
                },
            );

            return;
            }

        setState(() {
          _visibleThoughtCount++;
        });
      },
    );
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF9FAFF),
      body: SafeArea(
        child: Stack(
          children: [
            _buildBackground(),

            Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _buildThoughtHead(),

                  const SizedBox(height: 42),

                  _buildText(),

                  const SizedBox(height: 38),

                  SizedBox(
                    height: 150,
                    child: _buildThoughtBubbles(),
                  ),
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

  Widget _buildBackground() {
    return Positioned.fill(
      child: CustomPaint(
        painter: _SplashBackgroundPainter(),
      ),
    );
  }

  Widget _buildThoughtHead() {
    return Container(
      width: 130,
      height: 130,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: const Color(0xFFF0F1FF),
        boxShadow: [
          BoxShadow(
            color: AppColors.primary.withValues(alpha: 0.12),
            blurRadius: 35,
            spreadRadius: 6,
          ),
        ],
      ),
      child: const Icon(
        Icons.face_outlined,
        size: 70,
        color: AppColors.primary,
      ),
    );
  }

  Widget _buildText() {
    return const Column(
      children: [
        Text(
          '당신은',
          style: TextStyle(
            fontSize: 18,
            color: Color(0xFF34384A),
          ),
        ),
        SizedBox(height: 8),
        Text.rich(
          TextSpan(
            style: TextStyle(
              fontSize: 26,
              fontWeight: FontWeight.w700,
              color: Color(0xFF34384A),
            ),
            children: [
              TextSpan(
                text: '오늘 ',
              ),
              TextSpan(
                text: '몇 번의 생각',
                style: TextStyle(
                  color: AppColors.primary,
                ),
              ),
              TextSpan(
                text: '을',
              ),
            ],
          ),
        ),
        SizedBox(height: 6),
        Text(
          '했을까요?',
          style: TextStyle(
            fontSize: 26,
            fontWeight: FontWeight.w700,
            color: Color(0xFF34384A),
          ),
        ),
      ],
    );
  }

  Widget _buildThoughtBubbles() {
    return Stack(
      alignment: Alignment.center,
      children: [
        _buildBubble(
          0,
          left: 30,
          top: 20,
        ),
        _buildBubble(
          1,
          right: 20,
          top: 55,
        ),
        _buildBubble(
          2,
          left: 70,
          bottom: 10,
        ),
      ],
    );
  }

  Widget _buildBubble(
    int index, {
    double? left,
    double? right,
    double? top,
    double? bottom,
  }) {
    final isVisible = index < _visibleThoughtCount;

    return Positioned(
      left: left,
      right: right,
      top: top,
      bottom: bottom,
      child: AnimatedScale(
        duration: const Duration(milliseconds: 450),
        curve: Curves.easeOutBack,
        scale: isVisible ? 1 : 0,
        child: AnimatedOpacity(
          duration: const Duration(milliseconds: 350),
          opacity: isVisible ? 1 : 0,
          child: Container(
            padding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 10,
            ),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(24),
              border: Border.all(
                color: const Color(0xFFE1E4F5),
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.04),
                  blurRadius: 12,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Text(
              _thoughts[index],
              style: const TextStyle(
                fontSize: 12,
                color: Color(0xFF64697C),
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
      children: List.generate(
        5,
        (index) {
          return Container(
            width: index == 0 ? 7 : 6,
            height: index == 0 ? 7 : 6,
            margin: const EdgeInsets.symmetric(horizontal: 5),
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: index == 0
                  ? AppColors.primary
                  : const Color(0xFFD8DAE6),
            ),
          );
        },
      ),
    );
  }
}

class _SplashBackgroundPainter extends CustomPainter {
  @override
  void paint(
    Canvas canvas,
    Size size,
  ) {
    final paint = Paint()
      ..color = const Color(0xFFF4F5FF)
      ..style = PaintingStyle.fill;

    final path = Path()
      ..moveTo(0, size.height * 0.85)
      ..quadraticBezierTo(
        size.width * 0.3,
        size.height * 0.75,
        size.width * 0.55,
        size.height * 0.88,
      )
      ..quadraticBezierTo(
        size.width * 0.8,
        size.height * 0.95,
        size.width,
        size.height * 0.82,
      )
      ..lineTo(size.width, size.height)
      ..lineTo(0, size.height)
      ..close();

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(
    covariant CustomPainter oldDelegate,
  ) {
    return false;
  }
}