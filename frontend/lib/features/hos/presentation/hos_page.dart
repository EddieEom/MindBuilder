import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/widgets/feature_widgets.dart';
import '../../growth/application/growth_provider.dart';
import '../data/hos_repository.dart';

const patternLabels = {
  'future': '미래지향성',
  'creativity': '창의성',
  'execution': '실행력',
  'uncertainty': '불확실성',
  'perfectionism': '완벽주의',
  'resilience': '회복탄력성',
};

class HosPage extends ConsumerWidget {
  const HosPage({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) => FeaturePage(
    title: 'My Operating System',
    icon: Icons.psychology_outlined,
    subtitle: '나의 생각과 행동을 연결하는 Human OS',
    child: FeatureAsync(
      value: ref.watch(hosProvider),
      onRetry: () => ref.invalidate(hosProvider),
      builder: (os) => RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(hosProvider);
          await ref.read(hosProvider.future);
        },
        child: ListView(
          padding: const EdgeInsets.fromLTRB(22, 4, 22, 28),
          children: [
            FeatureCard(
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF0EBFF),
                      borderRadius: BorderRadius.circular(18),
                    ),
                    child: const Icon(
                      Icons.psychology,
                      color: featurePurple,
                      size: 37,
                    ),
                  ),
                  const SizedBox(width: 15),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Human OS Status',
                          style: TextStyle(fontSize: 10, color: featureMuted),
                        ),
                        const SizedBox(height: 7),
                        Text(
                          'OS 단계 · ${os.stage}',
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        const SizedBox(height: 8),
                        const Text(
                          '나의 생각과 행동을 연결합니다.',
                          style: TextStyle(fontSize: 10, color: featureMuted),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 8),
                  if (os.confidence != null)
                    ScoreRing(value: os.confidence!, label: '데이터 신뢰도')
                  else
                    Text(
                      os.confidenceLabel,
                      style: const TextStyle(color: featurePurple),
                    ),
                ],
              ),
            ),
            FeatureSection(
              'Version',
              trailing: TextButton(
                onPressed: () => showFeatureDetails(
                  context,
                  'OS 버전 기록',
                  const SizedBox(height: 440, child: HosVersions()),
                ),
                child: const Text('버전 히스토리', style: TextStyle(fontSize: 10)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    os.version,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                  const SizedBox(height: 5),
                  Text(
                    '최근 업데이트 ${displayDate(DateTime.tryParse('${os.metadata['generated_at']}'))}',
                    style: const TextStyle(fontSize: 10, color: featureMuted),
                  ),
                ],
              ),
            ),
            FeatureSection(
              'Core Value',
              child: os.values.isEmpty
                  ? const FeatureEmpty('핵심 가치가 아직 없어요.')
                  : Wrap(
                      spacing: 7,
                      runSpacing: 8,
                      children: os.values
                          .map(
                            (value) => ActionChip(
                              backgroundColor: const Color(0xFFF5F2FF),
                              side: BorderSide.none,
                              label: Text(
                                value.name,
                                style: const TextStyle(
                                  fontSize: 11,
                                  color: featurePurple,
                                ),
                              ),
                              onPressed: () => showFeatureDetails(
                                context,
                                value.name,
                                Text(value.description ?? '저장된 설명이 없어요.'),
                              ),
                            ),
                          )
                          .toList(),
                    ),
            ),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: FeatureCard(
                    padding: 12,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Thinking Pattern',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          os.thinking,
                          style: const TextStyle(
                            fontSize: 9,
                            color: featureMuted,
                          ),
                        ),
                        if (os.scores.isEmpty)
                          const FeatureEmpty('패턴 점수가 없어요.')
                        else
                          SizedBox(
                            height: 195,
                            child: CustomPaint(
                              size: const Size(double.infinity, 195),
                              painter: RadarPainter(
                                os.scores,
                                fontFamily: Theme.of(
                                  context,
                                ).textTheme.bodyMedium?.fontFamily,
                              ),
                            ),
                          ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: FeatureCard(
                    padding: 12,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Decision Pattern',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          os.decision,
                          style: const TextStyle(
                            fontSize: 9,
                            color: featureMuted,
                          ),
                        ),
                        const SizedBox(height: 14),
                        ...os.scores.entries.map(
                          (e) => Padding(
                            padding: const EdgeInsets.only(bottom: 10),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  patternLabels[e.key] ?? e.key,
                                  style: const TextStyle(
                                    fontSize: 8,
                                    color: featureMuted,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Row(
                                  children: [
                                    Expanded(
                                      child: LinearProgressIndicator(
                                        value: (e.value / 100).clamp(0, 1),
                                        minHeight: 3,
                                        borderRadius: BorderRadius.circular(4),
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    Text(
                                      '${e.value.round()}',
                                      style: const TextStyle(fontSize: 8),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            const Padding(
              padding: EdgeInsets.only(bottom: 12),
              child: Text(
                '차트는 현재 사고 패턴 점수를 표시합니다.',
                style: TextStyle(fontSize: 10, color: featureMuted),
              ),
            ),
            FeatureSection(
              'Growth Engine',
              trailing: TextButton(
                onPressed: () => context.push('/growth'),
                child: const Text('분석 자세히 보기', style: TextStyle(fontSize: 10)),
              ),
              child: ref
                  .watch(growthProvider)
                  .when(
                    loading: () => const LinearProgressIndicator(),
                    error: (e, _) => TextButton(
                      onPressed: () => ref.invalidate(growthProvider),
                      child: Text(requestMessage(e)),
                    ),
                    data: (growth) => growth.items.isEmpty
                        ? const FeatureEmpty('아직 성장 분석이 없어요.')
                        : Column(
                            children: growth.items
                                .map(
                                  (item) => ListTile(
                                    contentPadding: EdgeInsets.zero,
                                    dense: true,
                                    leading: Icon(
                                      item.type == 'UNLEARNING'
                                          ? Icons.delete_outline
                                          : item.type == 'RELEARNING'
                                          ? Icons.search
                                          : Icons.spa_outlined,
                                      color: featurePurple,
                                    ),
                                    title: Text(
                                      item.title,
                                      style: const TextStyle(fontSize: 12),
                                    ),
                                    onTap: () => showFeatureDetails(
                                      context,
                                      item.title,
                                      Text(item.content),
                                    ),
                                  ),
                                )
                                .toList(),
                          ),
                  ),
            ),
            FeatureSection(
              '실행 규칙',
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: os.rules
                    .map(
                      (rule) => Padding(
                        padding: const EdgeInsets.only(bottom: 12),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Icon(
                              Icons.check_box_outlined,
                              size: 15,
                              color: featurePurple,
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                rule,
                                style: const TextStyle(
                                  fontSize: 12,
                                  height: 1.7,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    )
                    .toList(),
              ),
            ),
            FeatureCard(
              color: const Color(0xFFF1EEFF),
              child: Row(
                children: [
                  const Icon(Icons.auto_awesome, color: featurePurple),
                  const SizedBox(width: 10),
                  const Expanded(
                    child: Text(
                      '당신의 OS는 계속 진화합니다.\n새로운 생각을 기록해 보세요.',
                      style: TextStyle(fontSize: 11, height: 1.7),
                    ),
                  ),
                  TextButton(
                    onPressed: () => context.push('/scan'),
                    child: const Text(
                      'Begin Scan ›',
                      style: TextStyle(fontSize: 11),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    ),
  );
}

class RadarPainter extends CustomPainter {
  RadarPainter(this.scores, {this.fontFamily});
  final String? fontFamily;
  final Map<String, double> scores;
  @override
  void paint(Canvas canvas, Size size) {
    final entries = patternLabels.entries.toList();
    final center = Offset(size.width / 2, size.height / 2);
    final radius = math.min(size.width, size.height) * .32;
    Offset point(int i, double scale) {
      final angle = -math.pi / 2 + 2 * math.pi * i / entries.length;
      return center + Offset(math.cos(angle), math.sin(angle)) * radius * scale;
    }

    final line = Paint()
      ..color = const Color(0xFFE4DEF7)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1;
    for (var ring = 1; ring <= 4; ring++) {
      final path = Path();
      for (var i = 0; i < entries.length; i++) {
        final p = point(i, ring / 4);
        if (i == 0) {
          path.moveTo(p.dx, p.dy);
        } else {
          path.lineTo(p.dx, p.dy);
        }
      }
      path.close();
      canvas.drawPath(path, line);
    }
    final data = Path();
    for (var i = 0; i < entries.length; i++) {
      canvas.drawLine(center, point(i, 1), line);
      final p = point(i, ((scores[entries[i].key] ?? 0) / 100).clamp(0, 1));
      if (i == 0) {
        data.moveTo(p.dx, p.dy);
      } else {
        data.lineTo(p.dx, p.dy);
      }
      final label = TextPainter(
        text: TextSpan(
          text:
              '${entries[i].value}\n${scores[entries[i].key]?.round() ?? '—'}',
          style: TextStyle(
            fontSize: 7,
            fontFamily: fontFamily,
            color: featureMuted,
            height: 1.5,
          ),
        ),
        textAlign: TextAlign.center,
        textDirection: TextDirection.ltr,
      )..layout();
      final position = point(i, 1.3);
      label.paint(canvas, position - Offset(label.width / 2, label.height / 2));
    }
    data.close();
    canvas.drawPath(
      data,
      Paint()..color = featurePurple.withValues(alpha: .22),
    );
    canvas.drawPath(
      data,
      Paint()
        ..color = featurePurple
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1.5,
    );
  }

  @override
  bool shouldRepaint(covariant RadarPainter oldDelegate) =>
      oldDelegate.scores != scores;
}

class HosVersions extends ConsumerWidget {
  const HosVersions({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) => FeatureAsync(
    value: ref.watch(hosVersionsProvider),
    onRetry: () => ref.invalidate(hosVersionsProvider),
    builder: (versions) => versions.isEmpty
        ? const FeatureEmpty('버전 기록이 없어요.')
        : ListView(
            children: versions
                .map(
                  (version) => ListTile(
                    title: Text(version.version),
                    subtitle: Text(
                      '${version.stage} · ${displayDate(version.date)}',
                    ),
                    trailing: version.current
                        ? const Text(
                            '현재',
                            style: TextStyle(color: featurePurple),
                          )
                        : const Icon(Icons.chevron_right),
                    onTap: () => showFeatureDetails(
                      context,
                      version.version,
                      SizedBox(
                        height: 400,
                        child: _HosHistoryDetail(id: version.id),
                      ),
                    ),
                  ),
                )
                .toList(),
          ),
  );
}

class _HosHistoryDetail extends ConsumerWidget {
  const _HosHistoryDetail({required this.id});
  final int id;
  @override
  Widget build(BuildContext context, WidgetRef ref) => FeatureAsync(
    value: ref.watch(hosHistoryProvider),
    onRetry: () => ref.invalidate(hosHistoryProvider),
    builder: (items) {
      final matches = items.where((item) => item.id == id);
      if (matches.isEmpty) return const FeatureEmpty('이 버전의 상세 기록이 없어요.');
      final item = matches.first;
      return ListView(
        children: [
          FeatureTags(item.values.map((v) => v.name).toList()),
          const SizedBox(height: 20),
          Text(
            '사고 패턴: ${item.thinking}\n의사결정 패턴: ${item.decision}',
            style: const TextStyle(height: 1.8),
          ),
          const SizedBox(height: 16),
          ...item.rules.map(
            (r) => Padding(
              padding: const EdgeInsets.only(bottom: 12),
              child: Text('• $r', style: const TextStyle(height: 1.7)),
            ),
          ),
          const Text(
            '패턴과 실행 규칙은 현재 누적 데이터를 반영합니다.',
            style: TextStyle(fontSize: 11, color: featureMuted),
          ),
        ],
      );
    },
  );
}
