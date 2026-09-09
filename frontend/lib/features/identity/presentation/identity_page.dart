import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/widgets/feature_widgets.dart';
import '../data/identity_repository.dart';

class IdentityPage extends ConsumerWidget {
  const IdentityPage({super.key, this.identityId});
  final int? identityId;
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final provider = identityId == null
        ? identityProvider
        : identityDetailProvider(identityId!);
    return FeaturePage(
      title: identityId == null ? 'Identity' : 'Identity 상세',
      icon: Icons.person_outline,
      subtitle: '당신을 설명하는 핵심 키워드를 보여드려요.',
      actions: [
        IconButton(
          tooltip: 'Identity 기록',
          onPressed: () => showFeatureDetails(
            context,
            'Identity 기록',
            const SizedBox(height: 400, child: IdentityHistoryList()),
          ),
          icon: const Icon(Icons.history, size: 20),
        ),
      ],
      child: FeatureAsync(
        value: ref.watch(provider),
        onRetry: () => ref.invalidate(provider),
        builder: (identity) => identity.name.isEmpty
            ? const FeatureEmpty('Scan을 완료하면 정체성 분석이 만들어져요.')
            : RefreshIndicator(
                onRefresh: () async {
                  ref.invalidate(provider);
                  await ref.read(provider.future);
                },
                child: ListView(
                  padding: const EdgeInsets.fromLTRB(22, 4, 22, 28),
                  children: [
                    FeatureCard(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            '당신은',
                            style: TextStyle(color: featureMuted, fontSize: 12),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            identity.name,
                            style: const TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.w800,
                              color: featurePurple,
                              letterSpacing: -.8,
                            ),
                          ),
                          const SizedBox(height: 10),
                          Text(
                            identity.description,
                            style: const TextStyle(
                              fontSize: 12,
                              color: featureMuted,
                              height: 1.7,
                            ),
                          ),
                          const SizedBox(height: 30),
                          Row(
                            children: [
                              Expanded(
                                child: ScoreRing(
                                  value: identity.creativity,
                                  label: '창의성',
                                ),
                              ),
                              Expanded(
                                child: ScoreRing(
                                  value: identity.execution,
                                  label: '실행력',
                                  color: const Color(0xFF76B77F),
                                ),
                              ),
                              Expanded(
                                child: ScoreRing(
                                  value: identity.uncertainty,
                                  label: '불확실성 민감도',
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                        ],
                      ),
                    ),
                    FeatureSection(
                      '핵심 키워드',
                      child: identity.keywords.isEmpty
                          ? const FeatureEmpty('아직 키워드가 없어요.')
                          : FeatureTags(identity.keywords),
                    ),
                    FeatureSection('강점', child: _bullets(identity.strengths)),
                    FeatureSection(
                      '성장 포인트',
                      child: _bullets(
                        identity.growthPoints,
                        color: const Color(0xFFE7AF68),
                      ),
                    ),
                    if (identity.candidates.isNotEmpty)
                      FeatureSection(
                        '현재 정체성 후보',
                        child: Column(
                          children: identity.candidates
                              .map(
                                (candidate) => ListTile(
                                  dense: true,
                                  contentPadding: EdgeInsets.zero,
                                  leading: CircleAvatar(
                                    radius: 14,
                                    child: Text('${candidate['rank'] ?? '-'}'),
                                  ),
                                  title: Text(
                                    '${candidate['identity_name'] ?? ''}',
                                  ),
                                  trailing: Text('${candidate['score'] ?? 0}'),
                                ),
                              )
                              .toList(),
                        ),
                      ),
                    if (identity.id != null)
                      IdentityFeedbackCard(identity: identity),
                    if (identityId == null && identity.id != null)
                      FilledButton(
                        onPressed: () =>
                            context.push('/identity/${identity.id}'),
                        child: const Text('더 자세히 보기'),
                      ),
                    if (identityId != null)
                      FeatureSection(
                        '분석 정보',
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '정체성 신뢰도 ${identity.confidence.round()}%',
                              style: const TextStyle(fontSize: 13),
                            ),
                            const SizedBox(height: 10),
                            Text(
                              '버전 ${identity.metadata['version']} · ${displayDate(DateTime.tryParse('${identity.metadata['generated_at']}'))}',
                              style: const TextStyle(
                                fontSize: 12,
                                color: featureMuted,
                              ),
                            ),
                            const SizedBox(height: 12),
                            const Text(
                              '점수는 현재까지 누적된 사고 패턴을 바탕으로 표시합니다.',
                              style: TextStyle(
                                fontSize: 11,
                                color: featureMuted,
                                height: 1.6,
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

  Widget _bullets(List<String> values, {Color color = featurePurple}) =>
      values.isEmpty
      ? const FeatureEmpty('아직 분석 내용이 없어요.')
      : Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: values
              .map(
                (text) => Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('•  ', style: TextStyle(color: color)),
                      Expanded(
                        child: Text(
                          text,
                          style: const TextStyle(
                            fontSize: 12,
                            color: Color(0xFF62637D),
                            height: 1.7,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              )
              .toList(),
        );
}

class IdentityFeedbackCard extends ConsumerWidget {
  const IdentityFeedbackCard({super.key, required this.identity});
  final IdentityModel identity;

  @override
  Widget build(BuildContext context, WidgetRef ref) => FeatureSection(
    '이 설명이 나와 맞나요?',
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          identity.hypothesisStatus == 'REVIEW_REQUIRED'
              ? '남겨주신 의견에 따라 정체성 가설을 다시 확인하고 있어요.'
              : '현재 분석은 가설입니다. 의견을 저장하고 다시 확인할 수 있어요.',
          style: const TextStyle(fontSize: 12, color: featureMuted),
        ),
        const SizedBox(height: 12),
        if (identity.userPerspective?['correction_text'] != null)
          Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: Text(
              '내가 남긴 의견: ${identity.userPerspective!['correction_text']}',
            ),
          ),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children:
              const [
                    ('AGREE', '맞아요'),
                    ('PARTIAL', '일부만 맞아요'),
                    ('DISAGREE', '달라요'),
                    ('UNSURE', '잘 모르겠어요'),
                  ]
                  .map(
                    (choice) => ChoiceChip(
                      label: Text(choice.$2),
                      selected: identity.feedback?['agreement'] == choice.$1,
                      onSelected: (_) => _submit(context, ref, choice.$1),
                    ),
                  )
                  .toList(),
        ),
      ],
    ),
  );

  Future<void> _submit(
    BuildContext context,
    WidgetRef ref,
    String agreement,
  ) async {
    final needsCorrection = agreement == 'PARTIAL' || agreement == 'DISAGREE';
    String? correction;
    if (needsCorrection) {
      final controller = TextEditingController();
      correction = await showDialog<String>(
        context: context,
        builder: (dialogContext) => AlertDialog(
          title: const Text('어떤 점이 다른가요?'),
          content: TextField(
            controller: controller,
            autofocus: true,
            maxLength: 1000,
            maxLines: 4,
            decoration: const InputDecoration(
              hintText: '내가 생각하는 나를 자유롭게 적어주세요.',
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(dialogContext),
              child: const Text('취소'),
            ),
            FilledButton(
              onPressed: () {
                final value = controller.text.trim();
                if (value.isNotEmpty) Navigator.pop(dialogContext, value);
              },
              child: const Text('저장'),
            ),
          ],
        ),
      );
      controller.dispose();
      if (correction == null) return;
    }
    if (!context.mounted) return;
    try {
      await ref
          .read(identityRepositoryProvider)
          .submitFeedback(
            identityId: identity.id!,
            agreement: agreement,
            correctionText: correction,
          );
      ref.invalidate(identityProvider);
      ref.invalidate(identityDetailProvider(identity.id!));
      if (context.mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text('의견을 저장했어요.')));
      }
    } catch (_) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('의견을 저장하지 못했어요. 다시 시도해 주세요.')),
        );
      }
    }
  }
}

class IdentityHistoryList extends ConsumerWidget {
  const IdentityHistoryList({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) => FeatureAsync(
    value: ref.watch(identityHistoryProvider),
    onRetry: () => ref.invalidate(identityHistoryProvider),
    builder: (items) => items.isEmpty
        ? const FeatureEmpty('아직 기록이 없어요.')
        : ListView(
            children: items
                .map(
                  (item) => ListTile(
                    title: Text(item.name),
                    subtitle: Text(
                      'v${item.version} · ${displayDate(item.date)}',
                    ),
                    trailing: item.current
                        ? const Text(
                            '현재',
                            style: TextStyle(color: featurePurple),
                          )
                        : const Icon(Icons.chevron_right),
                    onTap: () {
                      Navigator.pop(context);
                      context.push('/identity/${item.id}');
                    },
                  ),
                )
                .toList(),
          ),
  );
}
