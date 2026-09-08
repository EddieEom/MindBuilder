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
