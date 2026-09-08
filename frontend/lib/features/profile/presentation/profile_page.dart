import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:share_plus/share_plus.dart';
import '../../../core/routes/route_names.dart';
import '../../../core/storage/token_storage.dart';
import '../../../core/widgets/feature_widgets.dart';
import '../../auth/application/current_user_provider.dart';
import '../../auth/data/models/user_profile_model.dart';

class ProfilePage extends ConsumerWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) => Scaffold(
    backgroundColor: Theme.of(context).scaffoldBackgroundColor,
    bottomNavigationBar: const _ProfileNavigation(),
    body: SafeArea(
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 680),
          child: Column(
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(22, 18, 14, 10),
                child: Row(
                  children: [
                    const Expanded(
                      child: Row(
                        children: [
                          Text(
                            'Profile',
                            style: TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                          SizedBox(width: 7),
                          Icon(
                            Icons.person_outline,
                            color: featurePurple,
                            size: 21,
                          ),
                        ],
                      ),
                    ),
                    IconButton(
                      tooltip: '환경설정',
                      onPressed: () => context.push(RouteNames.settings),
                      icon: const Icon(Icons.settings_outlined, size: 21),
                    ),
                  ],
                ),
              ),
              const Padding(
                padding: EdgeInsets.fromLTRB(22, 0, 22, 14),
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    '나의 정보를 관리하고, MindBuilder의 내 기록을 확인하세요.',
                    style: TextStyle(fontSize: 11, color: featureMuted),
                  ),
                ),
              ),
              Expanded(
                child: FeatureAsync(
                  value: ref.watch(currentUserProvider),
                  onRetry: () => ref.invalidate(currentUserProvider),
                  builder: (profile) => RefreshIndicator(
                    onRefresh: () async {
                      ref.invalidate(currentUserProvider);
                      await ref.read(currentUserProvider.future);
                    },
                    child: ListView(
                      padding: const EdgeInsets.fromLTRB(22, 0, 22, 28),
                      children: [
                        _profileCard(context, ref, profile),
                        FeatureSection(
                          '나의 활동 요약',
                          trailing: TextButton(
                            onPressed: () => context.push(RouteNames.archive),
                            child: const Text(
                              '자세히 보기 ›',
                              style: TextStyle(fontSize: 10),
                            ),
                          ),
                          child: Row(
                            children: [
                              _stat(
                                'Scan 기록',
                                profile.scanCount,
                                Icons.psychology_outlined,
                                featurePurple,
                              ),
                              _stat(
                                '패턴 기록',
                                profile.patternCount,
                                Icons.trending_up,
                                const Color(0xFF67AD7B),
                              ),
                              _stat(
                                '총 기록',
                                profile.archiveCount,
                                Icons.local_fire_department_outlined,
                                const Color(0xFFE99A5C),
                              ),
                              _stat(
                                'AI 분석',
                                profile.analysisCount,
                                Icons.bar_chart,
                                const Color(0xFF718CE6),
                              ),
                              _stat(
                                '목표 노트',
                                profile.goalCount,
                                Icons.track_changes_outlined,
                                const Color(0xFF9785D9),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 110),
                        _menu(
                          context,
                          Icons.language,
                          '테마 설정',
                          '시스템 설정',
                          () => context.push(RouteNames.settings),
                        ),
                        const SizedBox(height: 10),
                        FeatureCard(
                          padding: 0,
                          child: Column(
                            children: [
                              _tile(
                                Icons.download_outlined,
                                '데이터 내보내기',
                                'JSON / PDF',
                                () => _export(context, ref),
                              ),
                              const Divider(),
                              _tile(
                                Icons.notifications_none,
                                '알림 설정',
                                '환경설정',
                                () => context.push(RouteNames.settings),
                              ),
                            ],
                          ),
                        ),
                        FeatureCard(
                          padding: 0,
                          child: Column(
                            children: [
                              _tile(
                                Icons.help_outline,
                                '도움말 및 가이드',
                                null,
                                () => _info(
                                  context,
                                  '도움말 및 가이드',
                                  'Mind Scan을 완료하면 Growth, Identity, Life Map, Human OS가 생성됩니다. 각 화면의 카드를 눌러 상세 내용을 확인할 수 있어요.',
                                ),
                              ),
                              const Divider(),
                              _tile(
                                Icons.info_outline,
                                '서비스 소개',
                                null,
                                () => _info(
                                  context,
                                  'MindBuilder',
                                  '생각을 기록하고 패턴을 발견해 성장 방향을 정리하는 서비스입니다.',
                                ),
                              ),
                              const Divider(),
                              _tile(
                                Icons.headset_mic_outlined,
                                '문의하기',
                                null,
                                () async {
                                  await Clipboard.setData(
                                    const ClipboardData(
                                      text: 'support@mindbuilder.app',
                                    ),
                                  );
                                  if (context.mounted) {
                                    _snack(context, '문의 이메일을 복사했어요.');
                                  }
                                },
                              ),
                            ],
                          ),
                        ),
                        OutlinedButton.icon(
                          style: OutlinedButton.styleFrom(
                            foregroundColor: const Color(0xFFE05E64),
                            side: const BorderSide(color: Color(0xFFF3D7D9)),
                          ),
                          onPressed: () => _logout(context),
                          icon: const Icon(Icons.logout, size: 17),
                          label: const Text('로그아웃'),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    ),
  );

  Widget _profileCard(
    BuildContext context,
    WidgetRef ref,
    UserProfileModel profile,
  ) => FeatureCard(
    color: Theme.of(context).cardColor,
    child: Row(
      children: [
        Stack(
          clipBehavior: Clip.none,
          children: [
            _avatar(profile),
            Positioned(
              right: -3,
              bottom: -3,
              child: InkWell(
                onTap: () => _editImage(context, ref, profile.profileImage),
                child: Container(
                  padding: const EdgeInsets.all(5),
                  decoration: BoxDecoration(
                    color: Theme.of(context).cardColor,
                    shape: BoxShape.circle,
                    border: Border.all(color: const Color(0xFFE4E2F1)),
                  ),
                  child: const Icon(Icons.camera_alt_outlined, size: 13),
                ),
              ),
            ),
          ],
        ),
        const SizedBox(width: 15),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Flexible(
                    child: Text(
                      profile.nickname,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ),
                  IconButton(
                    tooltip: '닉네임 수정',
                    padding: const EdgeInsets.all(4),
                    constraints: const BoxConstraints(),
                    onPressed: () =>
                        _editNickname(context, ref, profile.nickname),
                    icon: const Icon(
                      Icons.edit_outlined,
                      size: 14,
                      color: featurePurple,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 5),
              Row(
                children: [
                  Flexible(
                    child: Text(
                      profile.identityName.isEmpty
                          ? 'Identity 분석 전'
                          : profile.identityName,
                      style: const TextStyle(
                        fontSize: 11,
                        color: featurePurple,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                  if (profile.stage.isNotEmpty) ...[
                    const SizedBox(width: 5),
                    const Icon(Icons.circle, size: 4, color: featurePurple),
                    const SizedBox(width: 5),
                    Text(
                      profile.stage,
                      style: const TextStyle(fontSize: 10, color: featureMuted),
                    ),
                  ],
                ],
              ),
              const SizedBox(height: 8),
              Text(
                profile.email,
                style: const TextStyle(fontSize: 9, color: featureMuted),
              ),
              Text(
                '${profile.provider.toUpperCase()} 계정으로 연결되어 있어요.',
                style: const TextStyle(fontSize: 9, color: featureMuted),
              ),
            ],
          ),
        ),
      ],
    ),
  );

  Widget _avatar(UserProfileModel profile) {
    final url = profile.profileImage?.trim();
    return CircleAvatar(
      radius: 34,
      backgroundColor: const Color(0xFFE9E7F8),
      foregroundImage: url != null && url.isNotEmpty ? NetworkImage(url) : null,
      child: Text(
        profile.nickname.isEmpty ? '?' : profile.nickname[0],
        style: const TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.w700,
          color: featurePurple,
        ),
      ),
    );
  }

  Widget _stat(String label, int value, IconData icon, Color color) => Expanded(
    child: Column(
      children: [
        Icon(icon, size: 17, color: color),
        const SizedBox(height: 8),
        Text(label, style: const TextStyle(fontSize: 8, color: featureMuted)),
        const SizedBox(height: 4),
        Text(
          '$value개',
          style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700),
        ),
      ],
    ),
  );
  Widget _menu(
    BuildContext context,
    IconData icon,
    String title,
    String trailing,
    VoidCallback tap,
  ) => FeatureCard(padding: 0, child: _tile(icon, title, trailing, tap));
  Widget _tile(
    IconData icon,
    String title,
    String? trailing,
    VoidCallback tap,
  ) => ListTile(
    dense: true,
    leading: Icon(icon, size: 18, color: featureMuted),
    title: Text(title, style: const TextStyle(fontSize: 11)),
    trailing: Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (trailing != null)
          Text(
            trailing,
            style: const TextStyle(fontSize: 9, color: featureMuted),
          ),
        const SizedBox(width: 5),
        const Icon(Icons.chevron_right, size: 16),
      ],
    ),
    onTap: tap,
  );

  Future<void> _editNickname(
    BuildContext context,
    WidgetRef ref,
    String current,
  ) async {
    final controller = TextEditingController(text: current);
    final value = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('닉네임 변경'),
        content: TextField(
          controller: controller,
          autofocus: true,
          maxLength: 30,
          decoration: const InputDecoration(hintText: '2~30자로 입력'),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('취소'),
          ),
          FilledButton(
            onPressed: () {
              final value = controller.text.trim();
              if (value.length >= 2) Navigator.pop(context, value);
            },
            child: const Text('저장'),
          ),
        ],
      ),
    );
    controller.dispose();
    if (value == null || !context.mounted) return;
    try {
      await ref.read(userProfileRepositoryProvider).updateNickname(value);
      ref.invalidate(currentUserProvider);
      if (context.mounted) _snack(context, '닉네임을 변경했어요.');
    } catch (error) {
      if (context.mounted) _snack(context, requestMessage(error));
    }
  }

  Future<void> _editImage(
    BuildContext context,
    WidgetRef ref,
    String? current,
  ) async {
    final controller = TextEditingController(text: current ?? '');
    final value = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('프로필 이미지 변경'),
        content: TextField(
          controller: controller,
          autofocus: true,
          keyboardType: TextInputType.url,
          decoration: const InputDecoration(
            labelText: '이미지 URL',
            hintText: 'https://...',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('취소'),
          ),
          FilledButton(
            onPressed: () {
              final value = controller.text.trim();
              final uri = Uri.tryParse(value);
              if (uri != null &&
                  (uri.scheme == 'http' || uri.scheme == 'https')) {
                Navigator.pop(context, value);
              }
            },
            child: const Text('저장'),
          ),
        ],
      ),
    );
    controller.dispose();
    if (value == null || !context.mounted) return;
    try {
      await ref.read(userProfileRepositoryProvider).updateProfileImage(value);
      ref.invalidate(currentUserProvider);
      if (context.mounted) _snack(context, '프로필 이미지를 변경했어요.');
    } catch (error) {
      if (context.mounted) _snack(context, requestMessage(error));
    }
  }

  Future<void> _export(BuildContext context, WidgetRef ref) async {
    final format = await showModalBottomSheet<String>(
      context: context,
      showDragHandle: true,
      builder: (context) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const ListTile(
              title: Text(
                '내보내기 형식',
                style: TextStyle(fontWeight: FontWeight.w700),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.data_object, color: featurePurple),
              title: const Text('JSON 복사'),
              subtitle: const Text('전체 원본 데이터를 클립보드에 복사합니다.'),
              onTap: () => Navigator.pop(context, 'json'),
            ),
            ListTile(
              leading: const Icon(
                Icons.picture_as_pdf_outlined,
                color: featurePurple,
              ),
              title: const Text('PDF 저장 및 공유'),
              subtitle: const Text('읽기 쉬운 사용자 데이터 보고서를 만듭니다.'),
              onTap: () => Navigator.pop(context, 'pdf'),
            ),
          ],
        ),
      ),
    );
    if (format == null || !context.mounted) return;
    try {
      if (format == 'pdf') {
        final bytes = await ref.read(userProfileRepositoryProvider).exportPdf();
        await SharePlus.instance.share(
          ShareParams(
            title: 'MindBuilder 사용자 데이터',
            files: [XFile.fromData(bytes, mimeType: 'application/pdf')],
            fileNameOverrides: ['mindbuilder-report.pdf'],
          ),
        );
        return;
      }
      final json = await ref.read(userProfileRepositoryProvider).exportData();
      await Clipboard.setData(ClipboardData(text: json));
      if (context.mounted) {
        _info(
          context,
          '데이터 내보내기 완료',
          '내 데이터를 JSON 형식으로 클립보드에 복사했어요. 원하는 문서나 메모에 붙여넣어 보관할 수 있습니다.',
        );
      }
    } catch (error) {
      if (context.mounted) _snack(context, requestMessage(error));
    }
  }

  Future<void> _logout(BuildContext context) async {
    await TokenStorage.instance.clearTokens();
    if (context.mounted) context.go(RouteNames.login);
  }

  void _info(BuildContext context, String title, String body) =>
      showFeatureDetails(
        context,
        title,
        Text(body, style: const TextStyle(height: 1.8)),
      );
  void _snack(BuildContext context, String text) =>
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(text)));
}

class _ProfileNavigation extends StatelessWidget {
  const _ProfileNavigation();
  @override
  Widget build(BuildContext context) => SafeArea(
    top: false,
    child: Container(
      color: Theme.of(context).cardColor,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _item(context, Icons.home_outlined, 'Home', RouteNames.dashboard),
          _item(
            context,
            Icons.track_changes_outlined,
            "Today's Scan",
            RouteNames.scan,
          ),
          _item(context, Icons.spa_outlined, 'Growth', RouteNames.growth),
          _item(context, Icons.hub_outlined, 'Life Map', RouteNames.lifemap),
          _item(
            context,
            Icons.person_outline,
            'Profile',
            RouteNames.profile,
            selected: true,
          ),
        ],
      ),
    ),
  );
  Widget _item(
    BuildContext context,
    IconData icon,
    String label,
    String route, {
    bool selected = false,
  }) => InkWell(
    onTap: () => context.go(route),
    child: Padding(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 10),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 18, color: selected ? featurePurple : featureMuted),
          const SizedBox(height: 4),
          Text(
            label,
            style: TextStyle(
              fontSize: 8,
              color: selected ? featurePurple : featureMuted,
            ),
          ),
        ],
      ),
    ),
  );
}
