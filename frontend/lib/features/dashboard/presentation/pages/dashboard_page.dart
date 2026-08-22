import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../auth/application/current_user_provider.dart';
import '../../application/dashboard_controller.dart';
import '../../data/models/dashboard_model.dart';
import '../../../onboarding/presentation/pages/onboarding_page.dart';

class DashboardPage extends ConsumerWidget {
  const DashboardPage({super.key});

  static const _backgroundColor = Color(0xFFF8F9FC);
  static const _primaryColor = Color(0xFF5B4FD6);
  static const _textPrimary = Color(0xFF252A3A);
  static const _textSecondary = Color(0xFF7A8090);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dashboardAsync = ref.watch(dashboardProvider);
    final currentUserAsync = ref.watch(currentUserProvider);

    return Scaffold(
      backgroundColor: _backgroundColor,
      body: SafeArea(
        child: dashboardAsync.when(
          loading: () => const Center(
            child: CircularProgressIndicator(
              color: _primaryColor,
            ),
          ),
          error: (error, stackTrace) => _DashboardError(
            error: error,
            onRetry: () {
              ref.invalidate(dashboardProvider);
              ref.invalidate(currentUserProvider);
            },
          ),
          data: (dashboard) {
            return RefreshIndicator(
              color: _primaryColor,
              onRefresh: () async {
                ref.invalidate(dashboardProvider);
                ref.invalidate(currentUserProvider);

                await Future.wait([
                  ref.read(dashboardProvider.future),
                  ref.read(currentUserProvider.future),
                ]);
              },
              child: CustomScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                slivers: [
                  SliverPadding(
                    padding: const EdgeInsets.fromLTRB(
                      20,
                      16,
                      20,
                      28,
                    ),
                    sliver: SliverList(
                      delegate: SliverChildListDelegate(
                        [
                          _buildHeader(currentUserAsync),

                          const SizedBox(height: 24),

                          _buildGreeting(currentUserAsync),

                          const SizedBox(height: 18),

                          _buildHeroCard(context),

                          const SizedBox(height: 14),

                          _buildHumanOsCard(
                            dashboard.humanOs,
                          ),

                          const SizedBox(height: 14),

                          _buildInsightCard(
                            dashboard.insight,
                          ),

                          const SizedBox(height: 14),

                          _buildNextActionCard(
                            context,
                            dashboard.nextAction,
                          ),

                          const SizedBox(height: 14),

                          _buildRecentChangesCard(
                            dashboard.recentChanges,
                          ),

                          const SizedBox(height: 24),

                          _buildQuickMenu(),

                          const SizedBox(height: 24),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }

  // ============================================================
  // Header
  // ============================================================

  Widget _buildHeader(
    AsyncValue<dynamic> currentUserAsync,
  ) {
    final nickname = currentUserAsync.when(
      data: (user) => _resolveNickname(user),
      loading: () => '사용자',
      error: (_, _) => '사용자',
    );

    final profileImage = currentUserAsync.when(
      data: (user) => _resolveProfileImage(user),
      loading: () => null,
      error: (_, _) => null,
    );

    return Row(
      children: [
        const Expanded(
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Flexible(
                child: Text(
                  'MindBuilder',
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.w700,
                    color: _textPrimary,
                    letterSpacing: -0.8,
                  ),
                ),
              ),
              SizedBox(width: 6),
              SizedBox(
                width: 8,
                height: 8,
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    color: _primaryColor,
                    shape: BoxShape.circle,
                  ),
                ),
              ),
            ],
          ),
        ),

        Stack(
          clipBehavior: Clip.none,
          children: [
            const Icon(
              Icons.notifications_none_rounded,
              size: 28,
              color: _textPrimary,
            ),
            Positioned(
              top: 1,
              right: 1,
              child: Container(
                width: 8,
                height: 8,
                decoration: const BoxDecoration(
                  color: _primaryColor,
                  shape: BoxShape.circle,
                ),
              ),
            ),
          ],
        ),

        const SizedBox(width: 16),

        _ProfileAvatar(
          nickname: nickname,
          profileImage: profileImage,
        ),
      ],
    );
  }

  // ============================================================
  // Greeting
  // ============================================================

  Widget _buildGreeting(
    AsyncValue<dynamic> currentUserAsync,
  ) {
    final nickname = currentUserAsync.when(
      data: (user) => _resolveNickname(user),
      loading: () => '사용자',
      error: (_, _) => '사용자',
    );

    final displayName = nickname.trim().isNotEmpty
        ? nickname
        : '사용자';

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '안녕하세요, $displayName님 👋',
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(
            fontSize: 23,
            fontWeight: FontWeight.w700,
            color: _textPrimary,
            letterSpacing: -0.8,
          ),
        ),

        const SizedBox(height: 6),

        const Text(
          '오늘도 당신의 사고를 함께 정리해볼까요?',
          style: TextStyle(
            fontSize: 14,
            color: _textSecondary,
            letterSpacing: -0.3,
          ),
        ),
      ],
    );
  }

  // ============================================================
  // User Profile Resolver
  //
  // UserProfileModel의 실제 필드명을 확인한 뒤
  // 아래 부분만 프로젝트 모델에 맞게 수정하면 된다.
  // ============================================================

  String _resolveNickname(dynamic user) {
    try {
      final nickname = user.nickname;

      if (nickname is String && nickname.trim().isNotEmpty) {
        return nickname.trim();
      }
    } catch (_) {}

    try {
      final username = user.username;

      if (username is String && username.trim().isNotEmpty) {
        return username.trim();
      }
    } catch (_) {}

    try {
      final name = user.name;

      if (name is String && name.trim().isNotEmpty) {
        return name.trim();
      }
    } catch (_) {}

    return '사용자';
  }

  String? _resolveProfileImage(dynamic user) {
    try {
      final profileImage = user.profileImage;

      if (profileImage is String &&
          profileImage.trim().isNotEmpty) {
        return profileImage.trim();
      }
    } catch (_) {}

    try {
      final imageUrl = user.profileImageUrl;

      if (imageUrl is String &&
          imageUrl.trim().isNotEmpty) {
        return imageUrl.trim();
      }
    } catch (_) {}

    return null;
  }

  // ============================================================
  // Hero Card
  // ============================================================

  Widget _buildHeroCard(BuildContext context) {
    return Container(
      width: double.infinity,
      constraints: const BoxConstraints(
        minHeight: 214,
      ),
      padding: const EdgeInsets.all(22),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20),
        gradient: const LinearGradient(
          colors: [
            Color(0xFFF7F7FC),
            Color(0xFFEFF0FF),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        border: Border.all(
          color: const Color(0xFFE0E2F0),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.025),
            blurRadius: 16,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: LayoutBuilder(
        builder: (context, constraints) {
          final isCompact = constraints.maxWidth < 340;

          return Stack(
            children: [
              if (!isCompact)
                Positioned(
                  right: -8,
                  top: 6,
                  child: _buildSeedIllustration(),
                ),

              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 13,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: const Color(0xFFE9E9F7),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: const Text(
                      '오늘의 Human OS',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: _primaryColor,
                      ),
                    ),
                  ),

                  const SizedBox(height: 16),

                  const Text(
                    '생각은 정리될수록\n행동은 쉬워집니다.',
                    style: TextStyle(
                      fontSize: 22,
                      height: 1.35,
                      fontWeight: FontWeight.w700,
                      color: _textPrimary,
                      letterSpacing: -0.9,
                    ),
                  ),

                  const SizedBox(height: 22),

                  SizedBox(
                    width: isCompact
                        ? double.infinity
                        : 205,
                    height: 48,
                    child: ElevatedButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const OnboardingPage(),
                          ),
                        );
                      },
                      style: ElevatedButton.styleFrom(
                        elevation: 0,
                        backgroundColor: _primaryColor,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),
                      child: const Row(
                        mainAxisAlignment:
                            MainAxisAlignment.center,
                        children: [
                          Flexible(
                            child: Text(
                              '오늘 Mind Scan 시작하기',
                              overflow:
                                  TextOverflow.ellipsis,
                              style: TextStyle(
                                fontWeight:
                                    FontWeight.w600,
                              ),
                            ),
                          ),
                          SizedBox(width: 8),
                          Icon(
                            Icons.arrow_forward_rounded,
                            size: 19,
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildSeedIllustration() {
    return SizedBox(
      width: 125,
      height: 125,
      child: Stack(
        alignment: Alignment.center,
        children: [
          Container(
            width: 96,
            height: 96,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: const Color(0xFFE5E6FF)
                  .withValues(alpha: 0.35),
            ),
          ),

          Positioned(
            bottom: 14,
            child: Container(
              width: 3,
              height: 46,
              decoration: BoxDecoration(
                color: const Color(0xFF635BD7),
                borderRadius: BorderRadius.circular(10),
              ),
            ),
          ),

          Positioned(
            top: 33,
            left: 26,
            child: Transform.rotate(
              angle: -0.65,
              child: Container(
                width: 44,
                height: 23,
                decoration: BoxDecoration(
                  color: const Color(0xFF7D75DD),
                  borderRadius:
                      const BorderRadius.only(
                    topLeft: Radius.circular(24),
                    topRight: Radius.circular(4),
                    bottomLeft: Radius.circular(24),
                    bottomRight:
                        Radius.circular(24),
                  ),
                ),
              ),
            ),
          ),

          Positioned(
            top: 36,
            right: 22,
            child: Transform.rotate(
              angle: 0.65,
              child: Container(
                width: 44,
                height: 23,
                decoration: BoxDecoration(
                  color: const Color(0xFF8C84E8),
                  borderRadius:
                      const BorderRadius.only(
                    topLeft: Radius.circular(4),
                    topRight: Radius.circular(24),
                    bottomLeft:
                        Radius.circular(24),
                    bottomRight:
                        Radius.circular(24),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ============================================================
  // Human OS
  // ============================================================

  Widget _buildHumanOsCard(
    HumanOsSummary? humanOs,
  ) {
    final confidence = humanOs?.confidence ?? 0;

    final progress =
        (confidence / 100).clamp(0.0, 1.0);

    return _DashboardCard(
      child: Row(
        children: [
          SizedBox(
            width: 72,
            height: 72,
            child: Stack(
              alignment: Alignment.center,
              children: [
                SizedBox(
                  width: 66,
                  height: 66,
                  child: CircularProgressIndicator(
                    value: progress,
                    strokeWidth: 6,
                    backgroundColor:
                        const Color(0xFFE7E8F0),
                    valueColor:
                        const AlwaysStoppedAnimation<Color>(
                      _primaryColor,
                    ),
                    strokeCap: StrokeCap.round,
                  ),
                ),

                Text(
                  '${confidence.toStringAsFixed(0)}%',
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                    color: _primaryColor,
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(width: 16),

          Expanded(
            child: Column(
              crossAxisAlignment:
                  CrossAxisAlignment.start,
              children: [
                const Text(
                  'Human OS',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: _textPrimary,
                  ),
                ),

                const SizedBox(height: 5),

                Text(
                  humanOs?.stage ??
                      '아직 생성되지 않음',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w700,
                    color: _primaryColor,
                  ),
                ),

                const SizedBox(height: 7),

                Text(
                  '데이터 신뢰도 ${confidence.toStringAsFixed(0)}%',
                  style: const TextStyle(
                    fontSize: 12,
                    color: _textSecondary,
                  ),
                ),

                const SizedBox(height: 10),

                ClipRRect(
                  borderRadius:
                      BorderRadius.circular(10),
                  child: LinearProgressIndicator(
                    value: progress,
                    minHeight: 7,
                    backgroundColor:
                        const Color(0xFFE9EAF0),
                    valueColor:
                        const AlwaysStoppedAnimation<Color>(
                      _primaryColor,
                    ),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(width: 4),

          const Icon(
            Icons.chevron_right_rounded,
            color: Color(0xFF9CA1B0),
          ),
        ],
      ),
    );
  }

  // ============================================================
  // Insight
  // ============================================================

  Widget _buildInsightCard(
    InsightSummary? insight,
  ) {
    final title = insight?.title?.trim() ?? '';
    final content = insight?.content?.trim() ?? '';

    final hasTitle = title.isNotEmpty;
    final hasContent = content.isNotEmpty;

    return _DashboardCard(
      child: Row(
        crossAxisAlignment:
            CrossAxisAlignment.center,
        children: [
          _CircleIcon(
            icon:
                Icons.lightbulb_outline_rounded,
            backgroundColor:
                const Color(0xFFEDEBFF),
            iconColor: _primaryColor,
          ),

          const SizedBox(width: 16),

          Expanded(
            child: Column(
              crossAxisAlignment:
                  CrossAxisAlignment.start,
              children: [
                const Text(
                  '오늘의 인사이트',
                  style: TextStyle(
                    fontSize: 12,
                    color: _textSecondary,
                    fontWeight:
                        FontWeight.w500,
                  ),
                ),

                const SizedBox(height: 8),

                if (hasTitle)
                  Text(
                    title,
                    maxLines: 2,
                    overflow:
                        TextOverflow.ellipsis,
                    style: const TextStyle(
                      fontSize: 16,
                      height: 1.4,
                      color: _textPrimary,
                      fontWeight:
                          FontWeight.w700,
                      letterSpacing: -0.4,
                    ),
                  ),

                if (hasContent) ...[
                  const SizedBox(height: 4),
                  Text(
                    content,
                    maxLines: 2,
                    overflow:
                        TextOverflow.ellipsis,
                    style: const TextStyle(
                      fontSize: 13,
                      color: _textSecondary,
                      height: 1.4,
                    ),
                  ),
                ],

                if (!hasTitle && !hasContent)
                  const Text(
                    '아직 생성된 인사이트가 없습니다.',
                    style: TextStyle(
                      fontSize: 15,
                      height: 1.4,
                      color: _textSecondary,
                      fontWeight:
                          FontWeight.w500,
                    ),
                  ),
              ],
            ),
          ),

          const SizedBox(width: 4),

          const Icon(
            Icons.chevron_right_rounded,
            color: Color(0xFF9CA1B0),
          ),
        ],
      ),
    );
  }

  // ============================================================
  // Next Action
  // ============================================================

  Widget _buildNextActionCard(
    BuildContext context,
    NextActionSummary? nextAction,
  ) {
    final rawTitle =
    nextAction?.title?.trim() ?? '';

    final hasAction = rawTitle.isNotEmpty;

    return _DashboardCard(
      child: Row(
        crossAxisAlignment:
            CrossAxisAlignment.center,
        children: [
          _CircleIcon(
            icon: Icons.track_changes_rounded,
            backgroundColor:
                const Color(0xFFE5F5EE),
            iconColor:
                const Color(0xFF38A36C),
          ),

          const SizedBox(width: 16),

          Expanded(
            child: Column(
              crossAxisAlignment:
                  CrossAxisAlignment.start,
              children: [
                const Text(
                  '오늘의 Next Action',
                  style: TextStyle(
                    fontSize: 12,
                    color: _textSecondary,
                    fontWeight:
                        FontWeight.w500,
                  ),
                ),

                const SizedBox(height: 7),

                Text(
                  hasAction
                      ? rawTitle
                      : '아직 추천된 행동이 없습니다.',
                  maxLines: 2,
                  overflow:
                      TextOverflow.ellipsis,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight:
                        FontWeight.w700,
                    color: hasAction
                        ? _textPrimary
                        : _textSecondary,
                    letterSpacing: -0.4,
                  ),
                ),
              ],
            ),
          ),

          if (hasAction) ...[
            const SizedBox(width: 8),

            _ActionButton(
              onPressed: () {
                // TODO:
                // actionType / actionUrl 기반 라우팅 연결
              },
            ),
          ],
        ],
      ),
    );
  }

  // ============================================================
  // Recent Changes
  // ============================================================

  Widget _buildRecentChangesCard(
    List<RecentChange> changes,
  ) {
    if (changes.isEmpty) {
      return _DashboardCard(
        child: const Row(
          children: [
            _CircleIcon(
              icon: Icons.bar_chart_rounded,
              backgroundColor:
                  Color(0xFFFFF2E5),
              iconColor:
                  Color(0xFFF29A38),
            ),

            SizedBox(width: 16),

            Expanded(
              child: Text(
                '아직 비교할 분석 데이터가 부족합니다.',
                style: TextStyle(
                  fontSize: 14,
                  color: _textSecondary,
                ),
              ),
            ),
          ],
        ),
      );
    }

    final first = changes[0];

    final second =
        changes.length > 1
            ? changes[1]
            : null;

    return _DashboardCard(
      child: Column(
        children: [
          const Row(
            children: [
              _CircleIcon(
                icon: Icons.bar_chart_rounded,
                backgroundColor:
                    Color(0xFFFFF2E5),
                iconColor:
                    Color(0xFFF29A38),
              ),

              SizedBox(width: 16),

              Expanded(
                child: Text(
                  '최근 변화',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight:
                        FontWeight.w700,
                    color: _textPrimary,
                  ),
                ),
              ),

              Text(
                '성장 보기',
                style: TextStyle(
                  fontSize: 12,
                  color: _textSecondary,
                ),
              ),

              SizedBox(width: 2),

              Icon(
                Icons.chevron_right_rounded,
                size: 18,
                color: Color(0xFF9CA1B0),
              ),
            ],
          ),

          const SizedBox(height: 20),

          Row(
            children: [
              Expanded(
                child: _buildChangeMetric(
                    label: first.metric?.trim().isNotEmpty == true
                        ? first.metric!.trim()
                        : '변화',

                    value: first.change?.toDouble() ?? 0.0,
                  )
                ),

              if (second != null) ...[
                Container(
                  width: 1,
                  height: 42,
                  color:
                      const Color(0xFFE7E8EF),
                ),

                Expanded(
                  child: _buildChangeMetric(
                    label: second.metric?.trim().isNotEmpty == true
                        ? second.metric!.trim()
                        : '변화',

                    value: second.change?.toDouble() ?? 0.0,
                  ),
                ),
              ],
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildChangeMetric({
    required String label,
    required double value,
  }) {
    final isPositive = value >= 0;
    final prefix = isPositive ? '+' : '';

    return Padding(
      padding: const EdgeInsets.symmetric(
        horizontal: 8,
      ),
      child: Column(
        crossAxisAlignment:
            CrossAxisAlignment.start,
        children: [
          Text(
            label,
            maxLines: 1,
            overflow:
                TextOverflow.ellipsis,
            style: const TextStyle(
              fontSize: 12,
              color: _textSecondary,
            ),
          ),

          const SizedBox(height: 6),

          Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Flexible(
                child: Text(
                  '$prefix${value.toStringAsFixed(0)}',
                  overflow:
                      TextOverflow.ellipsis,
                  style: TextStyle(
                    fontSize: 23,
                    fontWeight:
                        FontWeight.w700,
                    color: isPositive
                        ? const Color(0xFF36A56B)
                        : const Color(0xFF4B9E79),
                  ),
                ),
              ),

              const SizedBox(width: 4),

              Icon(
                isPositive
                    ? Icons.arrow_upward_rounded
                    : Icons.arrow_downward_rounded,
                size: 16,
                color: isPositive
                    ? const Color(0xFF36A56B)
                    : const Color(0xFF4B9E79),
              ),
            ],
          ),
        ],
      ),
    );
  }

  // ============================================================
  // Quick Menu
  // ============================================================

  Widget _buildQuickMenu() {
    final items = [
      _QuickMenuData(
        label: 'Mind Scan',
        icon: Icons.psychology_outlined,
        color: _primaryColor,
      ),
      _QuickMenuData(
        label: 'Growth',
        icon: Icons.eco_outlined,
        color: const Color(0xFF4AA978),
      ),
      _QuickMenuData(
        label: 'Life Map',
        icon: Icons.map_outlined,
        color: const Color(0xFF4B82D1),
      ),
      _QuickMenuData(
        label: 'Identity',
        icon: Icons.person_outline_rounded,
        color: _primaryColor,
      ),
      _QuickMenuData(
        label: 'Archive',
        icon: Icons.folder_open_outlined,
        color: const Color(0xFFF29A38),
      ),
    ];

    return Column(
      crossAxisAlignment:
          CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.only(left: 4),
          child: Text(
            '빠른 메뉴',
            style: TextStyle(
              fontSize: 14,
              fontWeight:
                  FontWeight.w700,
              color: _textPrimary,
            ),
          ),
        ),

        const SizedBox(height: 14),

        GridView.builder(
          shrinkWrap: true,
          physics:
              const NeverScrollableScrollPhysics(),
          itemCount: items.length,
          gridDelegate:
              const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 3,
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
            childAspectRatio: 1.15,
          ),
          itemBuilder: (context, index) {
            return _QuickMenuButton(
              data: items[index],
            );
          },
        ),
      ],
    );
  }
}

// ============================================================
// Shared Widgets
// ============================================================

class _DashboardCard extends StatelessWidget {
  const _DashboardCard({
    required this.child,
  });

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius:
            BorderRadius.circular(20),
        border: Border.all(
          color: const Color(0xFFEAEBF1),
        ),
        boxShadow: [
          BoxShadow(
            color:
                Colors.black.withValues(
              alpha: 0.025,
            ),
            blurRadius: 18,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: child,
    );
  }
}

class _CircleIcon extends StatelessWidget {
  const _CircleIcon({
    required this.icon,
    required this.backgroundColor,
    required this.iconColor,
  });

  final IconData icon;
  final Color backgroundColor;
  final Color iconColor;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 58,
      height: 58,
      decoration: BoxDecoration(
        color: backgroundColor,
        shape: BoxShape.circle,
      ),
      child: Icon(
        icon,
        color: iconColor,
        size: 27,
      ),
    );
  }
}

class _ProfileAvatar extends StatelessWidget {
  const _ProfileAvatar({
    required this.nickname,
    required this.profileImage,
  });

  final String nickname;
  final String? profileImage;

  @override
  Widget build(BuildContext context) {
    final imageUrl = profileImage?.trim();

    final initial =
        nickname.trim().isNotEmpty
            ? nickname.trim()[0].toUpperCase()
            : '?';

    return Container(
      width: 42,
      height: 42,
      decoration: const BoxDecoration(
        color: Color(0xFFE8EBF8),
        shape: BoxShape.circle,
      ),
      clipBehavior: Clip.antiAlias,
      child: imageUrl != null &&
              imageUrl.isNotEmpty
          ? Image.network(
              imageUrl,
              fit: BoxFit.cover,
              errorBuilder:
                  (context, error, stackTrace) {
                return _ProfileInitial(
                  initial: initial,
                );
              },
            )
          : _ProfileInitial(
              initial: initial,
            ),
    );
  }
}

class _ProfileInitial extends StatelessWidget {
  const _ProfileInitial({
    required this.initial,
  });

  final String initial;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        initial,
        style: const TextStyle(
          fontSize: 17,
          fontWeight: FontWeight.w700,
          color: Color(0xFF4D5673),
        ),
      ),
    );
  }
}

class _ActionButton extends StatelessWidget {
  const _ActionButton({
    required this.onPressed,
  });

  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return TextButton(
      onPressed: onPressed,
      style: TextButton.styleFrom(
        foregroundColor:
            const Color(0xFF3AA06D),
        backgroundColor:
            const Color(0xFFEAF6F0),
        minimumSize:
            const Size(72, 40),
        padding:
            const EdgeInsets.symmetric(
          horizontal: 10,
          vertical: 8,
        ),
        shape: RoundedRectangleBorder(
          borderRadius:
              BorderRadius.circular(10),
        ),
      ),
      child: const Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            '시작',
            style: TextStyle(
              fontSize: 12,
              fontWeight:
                  FontWeight.w600,
            ),
          ),
          SizedBox(width: 4),
          Icon(
            Icons.arrow_forward_rounded,
            size: 16,
          ),
        ],
      ),
    );
  }
}

class _QuickMenuData {
  const _QuickMenuData({
    required this.label,
    required this.icon,
    required this.color,
  });

  final String label;
  final IconData icon;
  final Color color;
}

class _QuickMenuButton extends StatelessWidget {
  const _QuickMenuButton({
    required this.data,
  });

  final _QuickMenuData data;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        borderRadius:
            BorderRadius.circular(18),
        onTap: () {
          // TODO:
          // 실제 라우트 확인 후 연결
        },
        child: Ink(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius:
                BorderRadius.circular(18),
            border: Border.all(
              color:
                  const Color(0xFFE9EAF0),
            ),
          ),
          child: Column(
            mainAxisAlignment:
                MainAxisAlignment.center,
            children: [
              Icon(
                data.icon,
                size: 28,
                color: data.color,
              ),

              const SizedBox(height: 8),

              Text(
                data.label,
                textAlign:
                    TextAlign.center,
                maxLines: 1,
                overflow:
                    TextOverflow.ellipsis,
                style: const TextStyle(
                  fontSize: 10,
                  color:
                      Color(0xFF3F4555),
                  fontWeight:
                      FontWeight.w600,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _DashboardError extends StatelessWidget {
  const _DashboardError({
    required this.error,
    required this.onRetry,
  });

  final Object error;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding:
            const EdgeInsets.all(32),
        child: Column(
          mainAxisSize:
              MainAxisSize.min,
          children: [
            const Icon(
              Icons.cloud_off_rounded,
              size: 48,
              color:
                  Color(0xFF8A90A0),
            ),

            const SizedBox(height: 16),

            const Text(
              'Dashboard를 불러오지 못했습니다.',
              style: TextStyle(
                fontSize: 17,
                fontWeight:
                    FontWeight.w700,
                color:
                    DashboardPage._textPrimary,
              ),
            ),

            const SizedBox(height: 8),

            Text(
              error.toString(),
              textAlign:
                  TextAlign.center,
              style: const TextStyle(
                fontSize: 12,
                color:
                    DashboardPage._textSecondary,
              ),
            ),

            const SizedBox(height: 20),

            ElevatedButton(
              onPressed: onRetry,
              style:
                  ElevatedButton.styleFrom(
                backgroundColor:
                    DashboardPage._primaryColor,
                foregroundColor:
                    Colors.white,
              ),
              child:
                  const Text('다시 시도'),
            ),
          ],
        ),
      ),
    );
  }
}