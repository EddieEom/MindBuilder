import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../application/dashboard_controller.dart';

class DashboardPage extends ConsumerWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dashboardAsync = ref.watch(dashboardProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('MindBuilder Dashboard'),
      ),
      body: dashboardAsync.when(
        loading: () {
          return const Center(
            child: CircularProgressIndicator(),
          );
        },
        error: (error, stackTrace) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Text(
                'Dashboard를 불러오지 못했습니다.\n\n$error',
                textAlign: TextAlign.center,
              ),
            ),
          );
        },
        data: (dashboard) {
          return ListView(
            padding: const EdgeInsets.all(24),
            children: [
              Text(
                'Dashboard API 연결 성공',
                style: Theme.of(context).textTheme.headlineMedium,
              ),

              const SizedBox(height: 24),

              Text(
                'Stage: ${dashboard.humanOs?.stage ?? '없음'}',
              ),

              const SizedBox(height: 8),

              Text(
                'Version: ${dashboard.humanOs?.version ?? '없음'}',
              ),

              const SizedBox(height: 8),

              Text(
                'Next Action: '
                '${dashboard.nextAction?.title ?? '없음'}',
              ),

              const SizedBox(height: 24),

              Text(
                'Recent Changes: '
                '${dashboard.recentChanges.length}',
              ),

              const SizedBox(height: 8),

              Text(
                'Recent Archives: '
                '${dashboard.recentArchives.length}',
              ),
            ],
          );
        },
      ),
    );
  }
}