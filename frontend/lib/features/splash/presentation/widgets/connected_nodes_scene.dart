import 'dart:async';

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

class ConnectedNodesScene extends StatefulWidget {
  final VoidCallback onComplete;

  const ConnectedNodesScene({
    super.key,
    required this.onComplete,
  });

  @override
  State<ConnectedNodesScene> createState() =>
      _ConnectedNodesSceneState();
}

class _ConnectedNodesSceneState extends State<ConnectedNodesScene>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 4000),
    );

    _controller.forward();

    _controller.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        Timer(
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
            Center(
              child: AnimatedBuilder(
                animation: _controller,
                builder: (context, child) {
                  return SizedBox(
                    width: 320,
                    height: 420,
                    child: CustomPaint(
                      painter: _NodeNetworkPainter(
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
                child: Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 32,
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Text(
                        'Mind Builder는',
                        style: TextStyle(
                          fontSize: 27,
                          fontWeight: FontWeight.w700,
                          color: Color(0xFF252B3B),
                        ),
                      ),

                      const SizedBox(height: 8),

                      Text.rich(
                        TextSpan(
                          style: const TextStyle(
                            fontSize: 27,
                            fontWeight: FontWeight.w700,
                            color: Color(0xFF252B3B),
                          ),
                          children: [
                            const TextSpan(
                              text: '감정만',
                              style: TextStyle(
                                color: Color(0xFF252B3B),
                              ),
                            ),
                            const TextSpan(
                              text: ' 분석하는',
                            ),
                          ],
                        ),
                        textAlign: TextAlign.center,
                      ),

                      const SizedBox(height: 8),

                      const Text(
                        '앱이 아닙니다.',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 27,
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
        final active = index == 3;

        return Container(
          width: active ? 9 : 6,
          height: active ? 9 : 6,
          margin: const EdgeInsets.symmetric(horizontal: 5),
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

class _NodeNetworkPainter extends CustomPainter {
  final double progress;

  _NodeNetworkPainter({
    required this.progress,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(
      size.width / 2,
      size.height / 2,
    );

    /*
      시작 위치
      이전 Scene처럼 흩어진 상태
    */

    final startNodes = [
      const Offset(45, 50),
      const Offset(270, 80),
      const Offset(55, 300),
      const Offset(260, 330),
      const Offset(150, 380),
    ];

    /*
      최종 위치
      중앙을 중심으로 구조 형성
    */

    final endNodes = [
      const Offset(85, 130),
      const Offset(230, 120),
      const Offset(70, 280),
      const Offset(240, 290),
      const Offset(150, 210),
    ];

    final nodeProgress = Curves.easeInOut.transform(
      (progress / 0.45).clamp(0.0, 1.0),
    );

    final nodes = <Offset>[];

    for (int i = 0; i < startNodes.length; i++) {
      nodes.add(
        Offset.lerp(
          startNodes[i],
          endNodes[i],
          nodeProgress,
        )!,
      );
    }

    /*
      연결선은 노드가 어느 정도 모인 뒤 생성
    */

    final lineProgress = Curves.easeOut.transform(
      ((progress - 0.4) / 0.4).clamp(0.0, 1.0),
    );

    final linePaint = Paint()
      ..color = AppColors.primary.withValues(alpha: 0.35)
      ..strokeWidth = 1.5
      ..style = PaintingStyle.stroke;

    final connections = [
      [0, 4],
      [1, 4],
      [2, 4],
      [3, 4],
      [0, 2],
      [1, 3],
    ];

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

    /*
      중앙 노드
    */

    final centerNodePaint = Paint()
      ..color = AppColors.primary.withValues(alpha: 0.12);

    canvas.drawCircle(
      center,
      34,
      centerNodePaint,
    );

    /*
      노드
    */

    final nodePaint = Paint()
      ..color = AppColors.primary;

    final nodeGlowPaint = Paint()
      ..color = AppColors.primary.withValues(alpha: 0.12);

    for (int i = 0; i < nodes.length; i++) {
      final node = nodes[i];

      canvas.drawCircle(
        node,
        14,
        nodeGlowPaint,
      );

      canvas.drawCircle(
        node,
        7,
        nodePaint,
      );
    }

    /*
      중앙 노드
    */

    canvas.drawCircle(
      endNodes[4],
      24,
      Paint()
        ..color = AppColors.primary.withValues(alpha: 0.12),
    );

    canvas.drawCircle(
      endNodes[4],
      10,
      nodePaint,
    );
  }

  @override
  bool shouldRepaint(
    covariant _NodeNetworkPainter oldDelegate,
  ) {
    return oldDelegate.progress != progress;
  }
}