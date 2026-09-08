import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';

const featurePurple = Color(0xFF6550F5);
const featureMuted = Color(0xFF85859C);
const featureBackground = Color(0xFFFAFAFE);

String displayDate(DateTime? date) =>
    date == null ? '기록 없음' : DateFormat('yyyy.MM.dd').format(date.toLocal());
String requestMessage(Object error) {
  if (error is DioException) {
    if (error.response?.statusCode == 404) {
      return '아직 분석 기록이 없어요. Scan을 먼저 완료해 주세요.';
    }
    if (error.response?.statusCode == 401) return '로그인이 만료됐어요. 다시 로그인해 주세요.';
  }
  return '데이터를 불러오지 못했어요. 연결을 확인하고 다시 시도해 주세요.';
}

class FeaturePage extends StatelessWidget {
  const FeaturePage({
    super.key,
    required this.title,
    required this.icon,
    required this.child,
    this.subtitle,
    this.actions = const [],
    this.bottom,
  });
  final String title;
  final IconData icon;
  final String? subtitle;
  final Widget child;
  final List<Widget> actions;
  final Widget? bottom;
  @override
  Widget build(BuildContext context) => Scaffold(
    backgroundColor: Theme.of(context).scaffoldBackgroundColor,
    bottomNavigationBar: bottom,
    body: SafeArea(
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 680),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
                child: Row(
                  children: [
                    IconButton(
                      tooltip: '뒤로',
                      onPressed: () => context.canPop()
                          ? context.pop()
                          : context.go('/dashboard'),
                      icon: const Icon(Icons.arrow_back_rounded, size: 20),
                    ),
                    Expanded(
                      child: Text(
                        title,
                        style: const TextStyle(
                          fontSize: 23,
                          fontWeight: FontWeight.w800,
                          letterSpacing: -.8,
                        ),
                      ),
                    ),
                    Icon(icon, color: featurePurple, size: 22),
                    ...actions,
                  ],
                ),
              ),
              if (subtitle != null)
                Padding(
                  padding: const EdgeInsets.fromLTRB(24, 0, 24, 18),
                  child: Text(
                    subtitle!,
                    style: const TextStyle(fontSize: 12, color: featureMuted),
                  ),
                ),
              Expanded(child: child),
            ],
          ),
        ),
      ),
    ),
  );
}

class FeatureCard extends StatelessWidget {
  const FeatureCard({
    super.key,
    required this.child,
    this.color,
    this.padding = 18,
  });
  final Widget child;
  final Color? color;
  final double padding;
  @override
  Widget build(BuildContext context) => Container(
    width: double.infinity,
    margin: const EdgeInsets.only(bottom: 12),
    padding: EdgeInsets.all(padding),
    decoration: BoxDecoration(
        color: color ?? Theme.of(context).cardColor,
      borderRadius: BorderRadius.circular(16),
      border: Border.all(color: const Color(0xFFEEEDF7)),
    ),
    child: child,
  );
}

class FeatureSection extends StatelessWidget {
  const FeatureSection(
    this.title, {
    super.key,
    required this.child,
    this.trailing,
  });
  final String title;
  final Widget child;
  final Widget? trailing;
  @override
  Widget build(BuildContext context) => FeatureCard(
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Expanded(
              child: Text(
                title,
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
            ?trailing,
          ],
        ),
        const SizedBox(height: 14),
        child,
      ],
    ),
  );
}

class FeatureAsync<T> extends StatelessWidget {
  const FeatureAsync({
    super.key,
    required this.value,
    required this.onRetry,
    required this.builder,
  });
  final AsyncValue<T> value;
  final VoidCallback onRetry;
  final Widget Function(T) builder;
  @override
  Widget build(BuildContext context) => value.when(
    loading: () => const Center(child: CircularProgressIndicator()),
    error: (error, _) => Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.cloud_off_outlined, color: featureMuted, size: 36),
            const SizedBox(height: 12),
            Text(requestMessage(error), textAlign: TextAlign.center),
            const SizedBox(height: 16),
            OutlinedButton(onPressed: onRetry, child: const Text('다시 시도')),
          ],
        ),
      ),
    ),
    data: builder,
  );
}

class FeatureEmpty extends StatelessWidget {
  const FeatureEmpty(this.message, {super.key});
  final String message;
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 24),
    child: Center(
      child: Text(
        message,
        textAlign: TextAlign.center,
        style: const TextStyle(color: featureMuted, height: 1.6),
      ),
    ),
  );
}

class FeatureTags extends StatelessWidget {
  const FeatureTags(this.tags, {super.key, this.color = featurePurple});
  final List<String> tags;
  final Color color;
  @override
  Widget build(BuildContext context) => Wrap(
    spacing: 6,
    runSpacing: 8,
    children: tags
        .map(
          (tag) => Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
            decoration: BoxDecoration(
              color: color.withValues(alpha: .08),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              tag,
              style: TextStyle(
                fontSize: 11,
                color: color,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        )
        .toList(),
  );
}

class ScoreRing extends StatelessWidget {
  const ScoreRing({
    super.key,
    required this.value,
    required this.label,
    this.color = featurePurple,
  });
  final double value;
  final String label;
  final Color color;
  @override
  Widget build(BuildContext context) => Column(
    children: [
      SizedBox(
        width: 62,
        height: 62,
        child: Stack(
          alignment: Alignment.center,
          children: [
            SizedBox.expand(
              child: CircularProgressIndicator(
                value: (value / 100).clamp(0, 1),
                strokeWidth: 4,
                color: color,
                backgroundColor: color.withValues(alpha: .1),
              ),
            ),
            Text(
              '${value.round()}',
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.w800,
                color: color,
              ),
            ),
          ],
        ),
      ),
      const SizedBox(height: 10),
      Text(label, style: const TextStyle(fontSize: 11, color: featureMuted)),
    ],
  );
}

Future<void> showFeatureDetails(
  BuildContext context,
  String title,
  Widget content,
) => showModalBottomSheet<void>(
  context: context,
  isScrollControlled: true,
  showDragHandle: true,
  backgroundColor: Theme.of(context).scaffoldBackgroundColor,
  builder: (context) => SafeArea(
    child: ConstrainedBox(
      constraints: BoxConstraints(
        maxHeight: MediaQuery.sizeOf(context).height * .8,
      ),
      child: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(24, 8, 24, 32),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              title,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
            ),
            const SizedBox(height: 20),
            content,
          ],
        ),
      ),
    ),
  ),
);
