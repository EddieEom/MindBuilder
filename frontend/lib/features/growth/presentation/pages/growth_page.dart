import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/widgets/feature_widgets.dart';
import '../../application/growth_provider.dart';
import '../../data/models/growth_model.dart';
import '../../../dashboard/application/dashboard_controller.dart';

class GrowthPage extends ConsumerStatefulWidget {
  const GrowthPage({super.key});
  @override
  ConsumerState<GrowthPage> createState() => _GrowthPageState();
}

class _GrowthPageState extends ConsumerState<GrowthPage> {
  bool _saving = false;
  final _sectionKeys = List.generate(5, (_) => GlobalKey());
  Future<void> _save(Future<void> Function() request) async {
    if (_saving) return;
    setState(() => _saving = true);
    try {
      await request();
      ref.invalidate(growthProvider);
      ref.invalidate(dashboardProvider);
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text('저장됐어요.')));
      }
    } catch (error) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(requestMessage(error))));
      }
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  @override
  Widget build(BuildContext context) => FeaturePage(
    title: 'Growth',
    icon: Icons.spa_outlined,
    subtitle: 'AI가 당신의 사고를 분석하고, 성장을 위한 방향을 제안합니다.',
    actions: [
      IconButton(
        tooltip: '분석 기준',
        icon: const Icon(Icons.tune, size: 19),
        onPressed: () {
          final growth = ref.read(growthProvider).valueOrNull;
          showFeatureDetails(
            context,
            '분석 기준',
            Text(
              growth == null
                  ? '분석을 불러온 뒤 확인할 수 있어요.'
                  : '작성한 Scan 답변을 바탕으로 사고 패턴과 성장 방향을 분석합니다.\n\n분석 버전: ${growth.metadata.analysisVersion}\n분석일: ${displayDate(growth.metadata.createdAt)}',
            ),
          );
        },
      ),
    ],
    child: FeatureAsync(
      value: ref.watch(growthProvider),
      onRetry: () => ref.invalidate(growthProvider),
      builder: (growth) => RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(growthProvider);
          await ref.read(growthProvider.future);
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.fromLTRB(22, 6, 22, 28),
          child: Column(
            children: [
              FeatureCard(
                color: const Color(0xFFF4F2FF),
                child: Row(
                  children: [
                    const Icon(Icons.storage_rounded, color: featurePurple),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            '분석 신뢰도',
                            style: TextStyle(color: featureMuted, fontSize: 10),
                          ),
                          Text(
                            '${growth.metadata.confidence.round()}%',
                            style: const TextStyle(fontWeight: FontWeight.w700),
                          ),
                          const SizedBox(height: 8),
                          LinearProgressIndicator(
                            value: (growth.metadata.confidence / 100).clamp(
                              0,
                              1,
                            ),
                            minHeight: 4,
                            borderRadius: BorderRadius.circular(5),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 20),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          '최근 분석',
                          style: TextStyle(fontSize: 10, color: featureMuted),
                        ),
                        Text(
                          displayDate(growth.metadata.createdAt),
                          style: const TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        TextButton(
                          onPressed: () => context.push('/scan'),
                          child: const Text(
                            '다시 분석하기',
                            style: TextStyle(fontSize: 10),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: Row(
                  children: List.generate(
                    5,
                    (i) => Expanded(
                      child: InkWell(
                        onTap: () {
                          final target = _sectionKeys[i].currentContext;
                          if (target != null) {
                            Scrollable.ensureVisible(
                              target,
                              duration: const Duration(milliseconds: 300),
                            );
                          }
                        },
                        child: Column(
                          children: [
                            CircleAvatar(
                              radius: 13,
                              backgroundColor: i == 0
                                  ? featurePurple
                                  : const Color(0xFFEFEFFA),
                              child: Text(
                                '${i + 1}',
                                style: TextStyle(
                                  fontSize: 11,
                                  color: i == 0 ? Colors.white : featureMuted,
                                ),
                              ),
                            ),
                            const SizedBox(height: 7),
                            Text(
                              [
                                '버려야 할 생각',
                                '본질적인 문제',
                                '어떻게 해결할까?',
                                'AI 분석 근거',
                                'AI 평가',
                              ][i],
                              style: const TextStyle(
                                fontSize: 8,
                                color: featureMuted,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 12),
              ...List.generate(3, (i) => _growthCard(growth, i)),
              FeatureSection(
                '4. AI 분석 근거 (Explainability)',
                key: _sectionKeys[3],
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'AI가 이 결론을 도출한 근거를 확인할 수 있어요.',
                      style: TextStyle(color: featureMuted, fontSize: 11),
                    ),
                    if (growth.explanations.isEmpty)
                      const FeatureEmpty('저장된 분석 근거가 아직 없어요.'),
                    ...growth.explanations.map(
                      (e) => ListTile(
                        contentPadding: EdgeInsets.zero,
                        leading: const Icon(
                          Icons.psychology_outlined,
                          color: featurePurple,
                        ),
                        title: Text(
                          e.title,
                          style: const TextStyle(fontSize: 12),
                        ),
                        trailing: const Icon(Icons.chevron_right),
                        onTap: () => showFeatureDetails(
                          context,
                          e.title,
                          Text(e.content, style: const TextStyle(height: 1.8)),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              if (growth.recommendations.isNotEmpty)
                FeatureSection(
                  'Next Action',
                  child: Column(
                    children: growth.recommendations.map((r) {
                      final saved = growth.actions.any(
                        (a) => a.recommendationId == r.recommendationId,
                      );
                      return Padding(
                        padding: const EdgeInsets.only(bottom: 12),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              r.title,
                              style: const TextStyle(
                                fontWeight: FontWeight.w600,
                                fontSize: 13,
                              ),
                            ),
                            const SizedBox(height: 6),
                            Text(
                              r.description,
                              style: const TextStyle(
                                color: featureMuted,
                                fontSize: 12,
                              ),
                            ),
                            Align(
                              alignment: Alignment.centerRight,
                              child: TextButton.icon(
                                onPressed:
                                    saved ||
                                        r.recommendationId == null ||
                                        _saving
                                    ? null
                                    : () => _save(
                                        () => ref
                                            .read(growthRepositoryProvider)
                                            .createAction(r),
                                      ),
                                icon: Icon(
                                  saved
                                      ? Icons.check_circle_outline
                                      : Icons.add_task,
                                  size: 16,
                                ),
                                label: Text(
                                  saved ? '다음 행동에 저장됨' : '다음 행동으로 저장',
                                ),
                              ),
                            ),
                          ],
                        ),
                      );
                    }).toList(),
                  ),
                ),
              FeatureSection(
                '5. AI 평가 (Feedback)',
                key: _sectionKeys[4],
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      '오늘의 분석이 도움이 되었나요?',
                      style: TextStyle(fontSize: 12, color: featureMuted),
                    ),
                    const SizedBox(height: 8),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: List.generate(
                        5,
                        (i) => Expanded(
                          child: IconButton(
                            constraints: const BoxConstraints(
                              minWidth: 40,
                              minHeight: 48,
                            ),
                            padding: const EdgeInsets.all(4),
                            tooltip: '${i + 1}점',
                            onPressed: _saving
                                ? null
                                : () => _save(
                                    () => ref
                                        .read(growthRepositoryProvider)
                                        .submitFeedback(
                                          growth.metadata.growthAnalysisId,
                                          i + 1,
                                        ),
                                  ),
                            icon: Icon(
                              i < (growth.feedback?.rating ?? 0)
                                  ? Icons.star_rounded
                                  : Icons.star_border_rounded,
                              size: 31,
                              color: i < (growth.feedback?.rating ?? 0)
                                  ? featurePurple
                                  : const Color(0xFFB9B8CF),
                            ),
                          ),
                        ),
                      ),
                    ),
                    const Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          '전혀 아니요',
                          style: TextStyle(fontSize: 9, color: featureMuted),
                        ),
                        Text(
                          '매우 도움이 되었어요',
                          style: TextStyle(fontSize: 9, color: featureMuted),
                        ),
                      ],
                    ),
                    if (_saving) const LinearProgressIndicator(),
                  ],
                ),
              ),
              FeatureCard(
                color: const Color(0xFFF0EDFF),
                child: Row(
                  children: [
                    const Icon(Icons.auto_awesome, color: featurePurple),
                    const SizedBox(width: 10),
                    const Expanded(
                      child: Text(
                        '더 깊은 성장을 원한다면?\nLife Map에서 성장 방향을 확인해 보세요.',
                        style: TextStyle(fontSize: 11, height: 1.7),
                      ),
                    ),
                    TextButton(
                      onPressed: () => context.push('/lifemap'),
                      child: const Text(
                        'Life Map 가기 ›',
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
    ),
  );

  Widget _growthCard(GrowthModel growth, int i) {
    final type = ['UNLEARNING', 'RELEARNING', 'NEWLEARNING'][i];
    final items = growth.items
        .where((item) => item.type.toUpperCase() == type)
        .toList();
    final color = [
      const Color(0xFFE07780),
      const Color(0xFFE9AC40),
      const Color(0xFF66AD7C),
    ][i];
    return FeatureCard(
      key: _sectionKeys[i],
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                [Icons.delete_outline, Icons.search, Icons.spa_outlined][i],
                color: color,
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  '${i + 1}. ${['버려야 할 생각', '본질적인 문제', '어떻게 해결할까?'][i]}',
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
              Text(
                ['Unlearning', 'Relearning', 'Newlearning'][i],
                style: TextStyle(fontSize: 9, color: color),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            [
              '현재 당신의 성장을 방해하고 있는 불필요한 생각입니다.',
              '표면적인 문제가 아닌, 근본 원인을 발견합니다.',
              '지금 당신에게 필요한 실행 가능한 행동 가이드입니다.',
            ][i],
            style: const TextStyle(fontSize: 10, color: featureMuted),
          ),
          if (items.isEmpty) const FeatureEmpty('아직 분석 내용이 없어요.'),
          ...items.map(
            (item) => InkWell(
              onTap: () => showFeatureDetails(
                context,
                item.title,
                Text(item.content, style: const TextStyle(height: 1.8)),
              ),
              child: Container(
                width: double.infinity,
                margin: const EdgeInsets.only(top: 12),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: color.withValues(alpha: .08),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Row(
                  children: [
                    Icon(Icons.format_quote, size: 20, color: color),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        item.title,
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                    const Icon(
                      Icons.chevron_right,
                      size: 17,
                      color: featureMuted,
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
