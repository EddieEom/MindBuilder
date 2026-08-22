import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

class ScatteredThoughtScene extends StatefulWidget {
  final VoidCallback onComplete;

  const ScatteredThoughtScene({
    super.key,
    required this.onComplete,
  });

  @override
  State<ScatteredThoughtScene> createState() =>
      _ScatteredThoughtSceneState();
}

class _ScatteredThoughtSceneState
    extends State<ScatteredThoughtScene>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  final List<_ThoughtNodeData> _nodes = [
    const _ThoughtNodeData(
      text: '?',
      left: 65,
      top: 140,
      size: 42,
    ),
    const _ThoughtNodeData(
      text: '?',
      right: 70,
      top: 210,
      size: 36,
    ),
    const _ThoughtNodeData(
      text: '?',
      left: 130,
      top: 300,
      size: 30,
    ),
    const _ThoughtNodeData(
      text: '?',
      right: 110,
      top: 390,
      size: 34,
    ),
    const _ThoughtNodeData(
      text: '?',
      left: 50,
      top: 500,
      size: 28,
    ),
  ];

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 4),
    )..forward();

    _controller.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        Future.delayed(
          const Duration(milliseconds: 1200),
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
            // 배경
            Positioned.fill(
              child: CustomPaint(
                painter: _ScatteredBackgroundPainter(),
              ),
            ),

            // 흩어진 질문 노드
            ...List.generate(
              _nodes.length,
              (index) => _buildNode(
                index,
                _nodes[index],
              ),
            ),

            // 중앙 텍스트
            Center(
              child: FadeTransition(
                opacity: CurvedAnimation(
                  parent: _controller,
                  curve: const Interval(
                    0.25,
                    0.55,
                    curve: Curves.easeOut,
                  ),
                ),
                child: const Padding(
                  padding: EdgeInsets.symmetric(
                    horizontal: 40,
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        '그래서 우리는',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.w700,
                          color: Color(0xFF252B3B),
                        ),
                      ),
                      SizedBox(height: 8),
                      Text.rich(
                        TextSpan(
                          children: [
                            TextSpan(
                              text: '왜 힘든지도',
                              style: TextStyle(
                                fontSize: 28,
                                fontWeight: FontWeight.w700,
                                color: AppColors.primary,
                              ),
                            ),
                          ],
                        ),
                        textAlign: TextAlign.center,
                      ),
                      SizedBox(height: 8),
                      Text(
                        '설명하지 못합니다.',
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

            // 페이지 인디케이터
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

  Widget _buildNode(
    int index,
    _ThoughtNodeData node,
  ) {
    final start = index * 0.08;
    final end = (start + 0.35).clamp(0.0, 1.0);

    return Positioned(
      left: node.left,
      right: node.right,
      top: node.top,
      child: FadeTransition(
        opacity: CurvedAnimation(
          parent: _controller,
          curve: Interval(
            start,
            end,
            curve: Curves.easeOut,
          ),
        ),
        child: ScaleTransition(
          scale: Tween<double>(
            begin: 0.4,
            end: 1.0,
          ).animate(
            CurvedAnimation(
              parent: _controller,
              curve: Interval(
                start,
                end,
                curve: Curves.easeOutBack,
              ),
            ),
          ),
          child: Container(
            width: node.size,
            height: node.size,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: AppColors.primary.withValues(alpha: 0.08),
              border: Border.all(
                color: AppColors.primary.withValues(alpha: 0.25),
              ),
            ),
            child: Text(
              node.text,
              style: TextStyle(
                fontSize: node.size * 0.45,
                fontWeight: FontWeight.w500,
                color: AppColors.primary.withValues(alpha: 0.65),
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
        final active = index == 2;

        return AnimatedContainer(
          duration: const Duration(milliseconds: 300),
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

class _ThoughtNodeData {
  final String text;
  final double? left;
  final double? right;
  final double top;
  final double size;

  const _ThoughtNodeData({
    required this.text,
    this.left,
    this.right,
    required this.top,
    required this.size,
  });
}

class _ScatteredBackgroundPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFFF1F2FF)
      ..style = PaintingStyle.fill;

    final path = Path()
      ..moveTo(0, size.height * 0.82)
      ..quadraticBezierTo(
        size.width * 0.25,
        size.height * 0.72,
        size.width * 0.48,
        size.height * 0.86,
      )
      ..quadraticBezierTo(
        size.width * 0.72,
        size.height * 0.98,
        size.width,
        size.height * 0.78,
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