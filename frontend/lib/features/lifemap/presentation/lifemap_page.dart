import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/widgets/feature_widgets.dart';
import '../data/lifemap_repository.dart';

Color nodeColor(MapNode node) => Color(
  int.tryParse(node.color.replaceFirst('#', 'FF'), radix: 16) ?? 0xFF6550F5,
);

class LifeMapPage extends ConsumerStatefulWidget {
  const LifeMapPage({super.key});
  @override
  ConsumerState<LifeMapPage> createState() => _LifeMapPageState();
}

class _LifeMapPageState extends ConsumerState<LifeMapPage> {
  int _tab = 0;
  @override
  Widget build(BuildContext context) => FeaturePage(
    title: 'Life Map',
    icon: Icons.lightbulb_outline,
    subtitle: '당신의 생각 지도를 탐색해 보세요.',
    child: Column(
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 22),
          child: Row(
            children: List.generate(
              3,
              (i) => Expanded(
                child: TextButton(
                  style: TextButton.styleFrom(
                    backgroundColor: _tab == i ? const Color(0xFFEFECFF) : null,
                    foregroundColor: _tab == i ? featurePurple : featureMuted,
                  ),
                  onPressed: () => setState(() => _tab = i),
                  child: Text(
                    ['Overview', '연결 지도', '히스토리'][i],
                    style: const TextStyle(fontSize: 12),
                  ),
                ),
              ),
            ),
          ),
        ),
        Expanded(
          child: _tab == 2
              ? FeatureAsync(
                  value: ref.watch(lifeMapHistoryProvider),
                  onRetry: () => ref.invalidate(lifeMapHistoryProvider),
                  builder: (maps) => maps.isEmpty
                      ? const FeatureEmpty('아직 지도 기록이 없어요.')
                      : ListView.builder(
                          padding: const EdgeInsets.all(22),
                          itemCount: maps.length,
                          itemBuilder: (context, i) => FeatureCard(
                            child: ListTile(
                              contentPadding: EdgeInsets.zero,
                              title: Text(
                                'Life Map v${maps[i].metadata['version']}',
                              ),
                              subtitle: Text(
                                displayDate(
                                  DateTime.tryParse(
                                    '${maps[i].metadata['generated_at']}',
                                  ),
                                ),
                              ),
                              trailing: const Icon(Icons.chevron_right),
                              onTap: () => showFeatureDetails(
                                context,
                                'Life Map 기록',
                                SizedBox(
                                  height: 420,
                                  child: LifeMapGraph(map: maps[i]),
                                ),
                              ),
                            ),
                          ),
                        ),
                )
              : FeatureAsync(
                  value: ref.watch(lifeMapProvider),
                  onRetry: () => ref.invalidate(lifeMapProvider),
                  builder: (map) => map.nodes.isEmpty
                      ? const FeatureEmpty('Scan을 완료하면 나만의 지도가 만들어져요.')
                      : RefreshIndicator(
                          onRefresh: () async {
                            ref.invalidate(lifeMapProvider);
                            await ref.read(lifeMapProvider.future);
                          },
                          child: ListView(
                            padding: const EdgeInsets.all(22),
                            children: [
                              Text(
                                _tab == 0
                                    ? '생각과 관심, 목표를 하나의 지도로.'
                                    : '노드를 선택하면 상세 정보를 볼 수 있어요.',
                                style: const TextStyle(
                                  fontSize: 11,
                                  color: featureMuted,
                                ),
                              ),
                              const SizedBox(height: 12),
                              SizedBox(
                                height: _tab == 0 ? 320 : 500,
                                child: LifeMapGraph(
                                  map: map,
                                  overview: _tab == 0,
                                ),
                              ),
                              if (_tab == 0)
                                FeatureSection(
                                  'Life Map 요약',
                                  child: Column(
                                    children: [
                                      _summary(
                                        '관심사',
                                        map.overview['interest_count'],
                                        Icons.spa_outlined,
                                        const Color(0xFF66AD7C),
                                      ),
                                      _summary(
                                        '목표',
                                        map.overview['goal_count'],
                                        Icons.flag_outlined,
                                        const Color(0xFFEAAC62),
                                      ),
                                      _summary(
                                        '가치관',
                                        map.overview['value_count'],
                                        Icons.favorite_outline,
                                        featurePurple,
                                      ),
                                      _summary(
                                        '연결',
                                        map.overview['connection_count'],
                                        Icons.hub_outlined,
                                        const Color(0xFF7589EF),
                                      ),
                                    ],
                                  ),
                                ),
                            ],
                          ),
                        ),
                ),
        ),
      ],
    ),
  );
  Widget _summary(String title, Object? count, IconData icon, Color color) =>
      Padding(
        padding: const EdgeInsets.symmetric(vertical: 9),
        child: Row(
          children: [
            Icon(icon, size: 18, color: color),
            const SizedBox(width: 12),
            Expanded(child: Text(title, style: const TextStyle(fontSize: 12))),
            Text(
              '$count',
              style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 12),
            ),
          ],
        ),
      );
}

class LifeMapGraph extends StatefulWidget {
  const LifeMapGraph({super.key, required this.map, this.overview = false});
  final LifeMapModel map;
  final bool overview;
  @override
  State<LifeMapGraph> createState() => _LifeMapGraphState();
}

class _LifeMapGraphState extends State<LifeMapGraph> {
  final _transform = TransformationController();
  @override
  void dispose() {
    _transform.dispose();
    super.dispose();
  }

  @override
  void didUpdateWidget(covariant LifeMapGraph oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.overview != widget.overview || oldWidget.map != widget.map) {
      _transform.value = Matrix4.identity();
    }
  }

  @override
  Widget build(BuildContext context) => LayoutBuilder(
    builder: (context, constraints) {
      final nodes = widget.map.nodes;
      if (nodes.isEmpty) return const FeatureEmpty('노드가 없어요.');
      final size = Size(constraints.maxWidth, constraints.maxHeight);
      final minX = nodes.map((n) => n.x).reduce(math.min),
          maxX = nodes.map((n) => n.x).reduce(math.max);
      final minY = nodes.map((n) => n.y).reduce(math.min),
          maxY = nodes.map((n) => n.y).reduce(math.max);
      final positions = <String, Offset>{};
      for (var i = 0; i < nodes.length; i++) {
        final n = nodes[i];
        if (maxX == minX && maxY == minY) {
          final angle = 2 * math.pi * i / nodes.length - math.pi / 2;
          positions[n.id] = nodes.length == 1
              ? Offset(size.width / 2, size.height / 2)
              : Offset(
                  size.width / 2 + math.cos(angle) * (size.width / 2 - 45),
                  size.height / 2 + math.sin(angle) * (size.height / 2 - 45),
                );
        } else {
          positions[n.id] = Offset(
            maxX == minX
                ? size.width / 2
                : 40 + (n.x - minX) / (maxX - minX) * (size.width - 80),
            maxY == minY
                ? size.height / 2
                : 40 + (n.y - minY) / (maxY - minY) * (size.height - 80),
          );
        }
      }
      return Stack(
        children: [
          InteractiveViewer(
            transformationController: _transform,
            minScale: .7,
            maxScale: 4,
            boundaryMargin: const EdgeInsets.all(100),
            child: SizedBox.fromSize(
              size: size,
              child: Stack(
                children: [
                  Positioned.fill(
                    child: CustomPaint(
                      painter: _Edges(widget.map.edges, positions),
                    ),
                  ),
                  ...nodes.map((node) {
                    final p = positions[node.id]!;
                    final center = node.type == 'IDENTITY';
                    final diameter = center
                        ? 68.0
                        : widget.overview
                        ? 58.0
                        : 52.0;
                    return Positioned(
                      left: p.dx - diameter / 2,
                      top: p.dy - diameter / 2,
                      width: diameter,
                      height: diameter,
                      child: Semantics(
                        button: true,
                        label: '${node.title} 노드 상세',
                        child: InkWell(
                          customBorder: const CircleBorder(),
                          onTap: () => context.push('/lifemap/node/${node.id}'),
                          child: Container(
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: center
                                  ? featurePurple
                                  : nodeColor(node).withValues(alpha: .1),
                              border: Border.all(
                                color: nodeColor(node).withValues(alpha: .2),
                              ),
                            ),
                            alignment: Alignment.center,
                            padding: const EdgeInsets.all(5),
                            child: Text(
                              node.title,
                              maxLines: 3,
                              overflow: TextOverflow.ellipsis,
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                fontSize: center ? 12 : 10,
                                fontWeight: FontWeight.w600,
                                color: center ? Colors.white : nodeColor(node),
                              ),
                            ),
                          ),
                        ),
                      ),
                    );
                  }),
                ],
              ),
            ),
          ),
          if (!widget.overview)
            Positioned(
              left: 0,
              top: 0,
              child: Column(
                children: [
                  IconButton.filledTonal(
                    tooltip: '확대',
                    onPressed: () => _zoom(1.25),
                    icon: const Icon(Icons.add, size: 18),
                  ),
                  IconButton.filledTonal(
                    tooltip: '축소',
                    onPressed: () => _zoom(.8),
                    icon: const Icon(Icons.remove, size: 18),
                  ),
                  IconButton(
                    tooltip: '지도 초기화',
                    onPressed: () => _transform.value = Matrix4.identity(),
                    icon: const Icon(Icons.center_focus_strong, size: 18),
                  ),
                ],
              ),
            ),
        ],
      );
    },
  );
  void _zoom(double factor) {
    final scale = (_transform.value.getMaxScaleOnAxis() * factor).clamp(
      .7,
      4.0,
    );
    _transform.value = Matrix4.diagonal3Values(scale, scale, 1);
  }
}

class _Edges extends CustomPainter {
  _Edges(this.edges, this.positions);
  final List<MapEdge> edges;
  final Map<String, Offset> positions;
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFFDAD6F5)
      ..strokeWidth = 1.2;
    for (final edge in edges) {
      final a = positions[edge.from], b = positions[edge.to];
      if (a != null && b != null) canvas.drawLine(a, b, paint);
    }
  }

  @override
  bool shouldRepaint(covariant _Edges oldDelegate) => true;
}

class LifeMapNodePage extends ConsumerWidget {
  const LifeMapNodePage({super.key, required this.nodeId});
  final String nodeId;
  @override
  Widget build(BuildContext context, WidgetRef ref) => FeaturePage(
    title: '노드 상세',
    icon: Icons.hub_outlined,
    child: FeatureAsync(
      value: ref.watch(lifeMapNodeProvider(nodeId)),
      onRetry: () => ref.invalidate(lifeMapNodeProvider(nodeId)),
      builder: (node) => ListView(
        padding: const EdgeInsets.all(22),
        children: [
          FeatureCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    CircleAvatar(
                      backgroundColor: nodeColor(node).withValues(alpha: .1),
                      child: Icon(Icons.spa_outlined, color: nodeColor(node)),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        node.title,
                        style: const TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                Text(
                  '${node.tags.length}개 키워드',
                  style: TextStyle(color: nodeColor(node), fontSize: 12),
                ),
                const SizedBox(height: 12),
                FeatureTags(node.tags, color: nodeColor(node)),
              ],
            ),
          ),
          FeatureSection(
            '노드 요약',
            child: node.summary.isEmpty
                ? const FeatureEmpty('아직 저장된 요약이 없어요.')
                : Text(
                    node.summary,
                    style: const TextStyle(fontSize: 13, height: 1.8),
                  ),
          ),
          FeatureSection(
            '관련 목표',
            child: node.goals.isEmpty
                ? const FeatureEmpty('연결된 목표가 아직 없어요.')
                : Column(
                    children: node.goals
                        .map(
                          (goal) => Padding(
                            padding: const EdgeInsets.only(bottom: 16),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  goal.title,
                                  style: const TextStyle(fontSize: 12),
                                ),
                                const SizedBox(height: 8),
                                Row(
                                  children: [
                                    Expanded(
                                      child: LinearProgressIndicator(
                                        value: (goal.progress / 100).clamp(
                                          0,
                                          1,
                                        ),
                                        color: nodeColor(node),
                                        minHeight: 5,
                                        borderRadius: BorderRadius.circular(4),
                                      ),
                                    ),
                                    const SizedBox(width: 10),
                                    Text(
                                      '${goal.progress.round()}%',
                                      style: const TextStyle(
                                        fontSize: 10,
                                        color: featureMuted,
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        )
                        .toList(),
                  ),
          ),
        ],
      ),
    ),
  );
}
