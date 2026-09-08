import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/routes/route_names.dart';
import '../../../core/storage/token_storage.dart';
import '../../../core/widgets/feature_widgets.dart';
import '../../auth/application/current_user_provider.dart';
import '../application/settings_controller.dart';

class SettingsPage extends ConsumerWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final settings = ref.watch(settingsProvider);
    final repository = ref.watch(userProfileRepositoryProvider);
    final card = Theme.of(context).cardColor;
    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 680),
            child: ListView(
              padding: const EdgeInsets.fromLTRB(22, 10, 22, 32),
              children: [
                Row(
                  children: [
                    IconButton(
                      tooltip: '뒤로',
                      onPressed: () => context.canPop()
                          ? context.pop()
                          : context.go(RouteNames.profile),
                      icon: const Icon(Icons.arrow_back_ios_new, size: 18),
                    ),
                    const Expanded(
                      child: Center(
                        child: Text(
                          'Setting',
                          style: TextStyle(
                            fontSize: 17,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 48),
                  ],
                ),
                const SizedBox(height: 20),
                Text.rich(
                  const TextSpan(
                    children: [
                      TextSpan(text: '앱 환경을 설정하고\n나만의 '),
                      TextSpan(
                        text: 'MindBuilder',
                        style: TextStyle(color: featurePurple),
                      ),
                      TextSpan(text: '를 만들어보세요.'),
                    ],
                  ),
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                    height: 1.55,
                  ),
                ),
                const SizedBox(height: 22),
                FeatureCard(
                  color: card,
                  padding: 0,
                  child: Column(
                    children: [
                      _switchTile(
                        Icons.dark_mode_outlined,
                        '다크모드',
                        '앱의 테마를 설정합니다.',
                        settings.darkMode,
                        (value) => ref
                            .read(settingsProvider.notifier)
                            .setDarkMode(value),
                      ),
                      const Divider(),
                      _switchTile(
                        Icons.notifications_none,
                        '알림',
                        '알림 수신 설정을 관리합니다.',
                        settings.notifications,
                        ref.read(settingsProvider.notifier).setNotifications,
                      ),
                      if (settings.notifications) ...[
                        const Divider(),
                        _tile(
                          Icons.schedule,
                          'Mind Scan 알림 시간',
                          '오늘 Scan을 완료하지 않았을 때 알려드려요.',
                          '${settings.reminderHour.toString().padLeft(2, '0')}:00',
                          () => _reminderHour(context, ref),
                        ),
                      ],
                      const Divider(),
                      _tile(
                        Icons.language,
                        '언어',
                        '앱 언어를 설정합니다.',
                        settings.language == 'ko' ? '한국어' : 'English',
                        () => _language(context, ref),
                      ),
                      const Divider(),
                      _tile(
                        Icons.shield_outlined,
                        '개인정보',
                        '개인정보 및 데이터 관리 옵션을 확인합니다.',
                        null,
                        () => _info(
                          context,
                          '개인정보 및 데이터',
                          '계정 정보와 MindBuilder 분석 데이터는 로그인한 사용자만 조회할 수 있습니다. 데이터 내보내기와 계정 삭제는 이 설정 화면에서 직접 실행할 수 있습니다.',
                        ),
                      ),
                    ],
                  ),
                ),
                FeatureCard(
                  color: card,
                  padding: 0,
                  child: Column(
                    children: [
                      _tile(
                        Icons.logout,
                        '로그아웃',
                        '현재 로그인된 계정에서 로그아웃합니다.',
                        null,
                        () => _logout(context),
                      ),
                      const Divider(),
                      _tile(
                        Icons.delete_outline,
                        '회원탈퇴',
                        '계정과 모든 데이터를 영구적으로 삭제합니다.',
                        null,
                        () => _deleteAccount(context, repository),
                        destructive: true,
                      ),
                    ],
                  ),
                ),
                FeatureCard(
                  color: card,
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.lightbulb_outline, color: featurePurple),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Mind Builder는',
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                            const SizedBox(height: 6),
                            Text(
                              '사용자의 사고 데이터를 안전하게 보호하며, 당신의 성장을 지원합니다.',
                              style: TextStyle(
                                fontSize: 10,
                                height: 1.7,
                                color: Theme.of(
                                  context,
                                ).textTheme.bodySmall?.color,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 8),
                const Center(
                  child: Text(
                    'MindBuilder v1.0.0',
                    style: TextStyle(fontSize: 9, color: featureMuted),
                  ),
                ),
                const SizedBox(height: 5),
                const Center(
                  child: Text(
                    '© 2026 MindBuilder. All rights reserved.',
                    style: TextStyle(fontSize: 8, color: featureMuted),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _switchTile(
    IconData icon,
    String title,
    String subtitle,
    bool value,
    ValueChanged<bool> changed,
  ) => ListTile(
    leading: _icon(icon),
    title: Text(
      title,
      style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
    ),
    subtitle: Text(
      subtitle,
      style: const TextStyle(fontSize: 9, color: featureMuted),
    ),
    trailing: Switch(value: value, onChanged: changed),
  );
  Widget _tile(
    IconData icon,
    String title,
    String subtitle,
    String? value,
    VoidCallback tap, {
    bool destructive = false,
  }) => ListTile(
    leading: _icon(icon, destructive: destructive),
    title: Text(
      title,
      style: TextStyle(
        fontSize: 12,
        fontWeight: FontWeight.w600,
        color: destructive ? const Color(0xFFE25E67) : null,
      ),
    ),
    subtitle: Text(
      subtitle,
      style: const TextStyle(fontSize: 9, color: featureMuted),
    ),
    trailing: Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (value != null)
          Text(
            value,
            style: const TextStyle(fontSize: 10, color: featurePurple),
          ),
        const SizedBox(width: 5),
        const Icon(Icons.chevron_right, size: 17, color: featureMuted),
      ],
    ),
    onTap: tap,
  );
  Widget _icon(IconData icon, {bool destructive = false}) => Container(
    width: 38,
    height: 38,
    decoration: BoxDecoration(
      color: (destructive ? const Color(0xFFE25E67) : featurePurple).withValues(
        alpha: .08,
      ),
      borderRadius: BorderRadius.circular(10),
    ),
    child: Icon(
      icon,
      size: 18,
      color: destructive ? const Color(0xFFE25E67) : featurePurple,
    ),
  );

  Future<void> _language(BuildContext context, WidgetRef ref) async {
    final selected = await showModalBottomSheet<String>(
      context: context,
      showDragHandle: true,
      builder: (context) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const ListTile(
              title: Text(
                '언어 선택',
                style: TextStyle(fontWeight: FontWeight.w700),
              ),
            ),
            ListTile(
              title: const Text('한국어'),
              trailing: ref.read(settingsProvider).language == 'ko'
                  ? const Icon(Icons.check, color: featurePurple)
                  : null,
              onTap: () => Navigator.pop(context, 'ko'),
            ),
            ListTile(
              title: const Text('English'),
              trailing: ref.read(settingsProvider).language == 'en'
                  ? const Icon(Icons.check, color: featurePurple)
                  : null,
              onTap: () => Navigator.pop(context, 'en'),
            ),
            const Padding(
              padding: EdgeInsets.all(16),
              child: Text(
                '현재 화면 콘텐츠는 한국어를 기본으로 제공하며, 전체 영문 번역은 추후 적용됩니다.',
                style: TextStyle(fontSize: 10, color: featureMuted),
              ),
            ),
          ],
        ),
      ),
    );
    if (selected != null) {
      await ref.read(settingsProvider.notifier).setLanguage(selected);
    }
  }

  Future<void> _reminderHour(BuildContext context, WidgetRef ref) async {
    final selected = await showModalBottomSheet<int>(
      context: context,
      showDragHandle: true,
      builder: (context) => SafeArea(
        child: SizedBox(
          height: 360,
          child: ListView(
            children: [
              const ListTile(
                title: Text(
                  '알림 시간 선택',
                  style: TextStyle(fontWeight: FontWeight.w700),
                ),
              ),
              for (final hour in [8, 12, 18, 20, 21, 22])
                ListTile(
                  title: Text('${hour.toString().padLeft(2, '0')}:00'),
                  trailing: ref.read(settingsProvider).reminderHour == hour
                      ? const Icon(Icons.check, color: featurePurple)
                      : null,
                  onTap: () => Navigator.pop(context, hour),
                ),
            ],
          ),
        ),
      ),
    );
    if (selected != null) {
      await ref.read(settingsProvider.notifier).setReminderHour(selected);
    }
  }

  Future<void> _logout(BuildContext context) async {
    await TokenStorage.instance.clearTokens();
    if (context.mounted) context.go(RouteNames.login);
  }

  Future<void> _deleteAccount(BuildContext context, dynamic repository) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        icon: const Icon(Icons.warning_amber_rounded, color: Color(0xFFE25E67)),
        title: const Text('정말 회원탈퇴할까요?'),
        content: const Text('계정과 저장된 모든 분석 데이터가 영구적으로 삭제되며 복구할 수 없습니다.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('취소'),
          ),
          FilledButton(
            style: FilledButton.styleFrom(
              backgroundColor: const Color(0xFFE25E67),
            ),
            onPressed: () => Navigator.pop(context, true),
            child: const Text('회원탈퇴'),
          ),
        ],
      ),
    );
    if (confirmed != true || !context.mounted) return;
    try {
      await repository.deleteAccount();
      await TokenStorage.instance.clearTokens();
      if (context.mounted) context.go(RouteNames.login);
    } catch (error) {
      if (context.mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(requestMessage(error))));
      }
    }
  }

  void _info(BuildContext context, String title, String content) =>
      showFeatureDetails(
        context,
        title,
        Text(content, style: const TextStyle(height: 1.8)),
      );
}
