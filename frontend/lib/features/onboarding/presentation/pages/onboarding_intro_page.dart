import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/routes/route_names.dart';

class OnboardingIntroPage extends StatefulWidget {
  const OnboardingIntroPage({super.key});

  @override
  State<OnboardingIntroPage> createState() =>
      _OnboardingIntroPageState();
}

class _OnboardingIntroPageState
    extends State<OnboardingIntroPage> {
  final PageController _pageController =
      PageController();

  int _currentPage = 0;

  final List<_IntroData> _pages = [
    const _IntroData(
      title: '환영합니다!',
      description:
          'Mind Builder에 오신 것을\n진심으로 환영합니다.\n\n이제 당신의 인간 운영체제를\n함께 만들어볼까요?',
      icon: Icons.rocket_launch_rounded,
      bottomText:
          '모든 데이터는 안전하게 보호되며,\n오직 당신만을 위해 사용됩니다.',
      bottomIcon: Icons.verified_user_outlined,
    ),
    const _IntroData(
      title: '앞으로\n몇 가지 질문을 드립니다.',
      description:
          '정답은 없습니다.\n있는 그대로 선택해주세요.',
      icon: Icons.analytics_outlined,
      bottomText:
          '솔직한 답변이 더 정확한\n인사이트와 성장을 만듭니다.',
      bottomIcon: Icons.auto_graph_rounded,
    ),
    const _IntroData(
      title: '당신의 답변은\n초기 사고 씨앗(Seed)이 됩니다.',
      description:
          '데이터가 쌓일수록\n더 정확한 분석을 제공합니다.',
      icon: Icons.energy_savings_leaf_outlined,
      bottomText:
          '언제든 철회해서 데이터를 관리 및\n삭제가 가능합니다.',
      bottomIcon: Icons.lock_outline_rounded,
    ),
  ];

  void _nextPage() {
    if (_currentPage == _pages.length - 1) {
      _startScan();
      return;
    }

    _pageController.nextPage(
      duration: const Duration(milliseconds: 400),
      curve: Curves.easeInOut,
    );
  }

  void _startScan() {
    context.go(RouteNames.scan);
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: 24,
            vertical: 16,
          ),
          child: Column(
            children: [
              const SizedBox(height: 8),

              _ProgressIndicator(
                currentPage: _currentPage,
                pageCount: _pages.length,
              ),

              const SizedBox(height: 24),

              Expanded(
                child: PageView.builder(
                  controller: _pageController,
                  itemCount: _pages.length,
                  onPageChanged: (index) {
                    setState(() {
                      _currentPage = index;
                    });
                  },
                  itemBuilder: (context, index) {
                    return _IntroContent(
                      data: _pages[index],
                    );
                  },
                ),
              ),

              const SizedBox(height: 16),

              _BottomInfo(
                data: _pages[_currentPage],
              ),

              const SizedBox(height: 24),

              Divider(
                color: AppColors.border,
              ),

              const SizedBox(height: 16),

              SizedBox(
                width: double.infinity,
                height: 54,
                child: ElevatedButton(
                  onPressed: _nextPage,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    foregroundColor: Colors.white,
                    elevation: 0,
                    shape: RoundedRectangleBorder(
                      borderRadius:
                          BorderRadius.circular(12),
                    ),
                  ),
                  child: Text(
                    _currentPage == _pages.length - 1
                        ? '시작하기 →'
                        : '다음 →',
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ),

              const SizedBox(height: 12),
            ],
          ),
        ),
      ),
    );
  }
}

class _IntroData {
  final String title;
  final String description;
  final IconData icon;
  final String bottomText;
  final IconData bottomIcon;

  const _IntroData({
    required this.title,
    required this.description,
    required this.icon,
    required this.bottomText,
    required this.bottomIcon,
  });
}

class _IntroContent extends StatelessWidget {
  const _IntroContent({
    required this.data,
  });

  final _IntroData data;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const Spacer(flex: 2),

        Container(
          width: 120,
          height: 120,
          decoration: BoxDecoration(
            color:
                AppColors.primary.withValues(alpha: 0.08),
            shape: BoxShape.circle,
          ),
          child: Icon(
            data.icon,
            size: 64,
            color: AppColors.primary,
          ),
        ),

        const SizedBox(height: 48),

        Text(
          data.title,
          textAlign: TextAlign.center,
          style: Theme.of(context)
              .textTheme
              .headlineSmall
              ?.copyWith(
                color: AppColors.textPrimary,
                fontWeight: FontWeight.bold,
                height: 1.45,
              ),
        ),

        const SizedBox(height: 24),

        Text(
          data.description,
          textAlign: TextAlign.center,
          style: Theme.of(context)
              .textTheme
              .bodyLarge
              ?.copyWith(
                color: AppColors.textSecondary,
                height: 1.7,
              ),
        ),

        const Spacer(flex: 3),
      ],
    );
  }
}

class _BottomInfo extends StatelessWidget {
  const _BottomInfo({
    required this.data,
  });

  final _IntroData data;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(
        horizontal: 18,
        vertical: 16,
      ),
      decoration: BoxDecoration(
        color:
            AppColors.primary.withValues(alpha: 0.05),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          Icon(
            data.bottomIcon,
            color: AppColors.primary,
            size: 26,
          ),

          const SizedBox(width: 12),

          Expanded(
            child: Text(
              data.bottomText,
              style: Theme.of(context)
                  .textTheme
                  .bodySmall
                  ?.copyWith(
                    color: AppColors.textSecondary,
                    height: 1.5,
                  ),
            ),
          ),
        ],
      ),
    );
  }
}

class _ProgressIndicator extends StatelessWidget {
  const _ProgressIndicator({
    required this.currentPage,
    required this.pageCount,
  });

  final int currentPage;
  final int pageCount;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: List.generate(
        pageCount,
        (index) {
          final isActive = index == currentPage;
          final isPast = index < currentPage;

          return Expanded(
            child: Container(
              margin: EdgeInsets.only(
                right:
                    index == pageCount - 1 ? 0 : 6,
              ),
              height: 3,
              decoration: BoxDecoration(
                color: isActive || isPast
                    ? AppColors.primary
                    : AppColors.border,
                borderRadius:
                    BorderRadius.circular(10),
              ),
            ),
          );
        },
      ),
    );
  }
}