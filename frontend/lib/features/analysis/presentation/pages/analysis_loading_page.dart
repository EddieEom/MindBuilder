import 'dart:async';

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/routes/route_names.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../dashboard/application/dashboard_controller.dart';
import '../../../auth/application/current_user_provider.dart';

class AnalysisLoadingPage extends ConsumerStatefulWidget {
  
  final int scanId;
  final Map<String, dynamic> analysisResult;

  const AnalysisLoadingPage({
    super.key,
    required this.scanId,
    required this.analysisResult,
  });

  @override
  ConsumerState<AnalysisLoadingPage> createState() =>
    _AnalysisLoadingPageState();
}

class _AnalysisLoadingPageState
    extends ConsumerState<AnalysisLoadingPage> {
  int _progress = 0;

  int _currentStep = 0;

  bool _completed = false;

  late final Map<String, dynamic> _analysisResult;

  final List<String> _steps = [
    '응답 데이터 정제',
    '핵심 키워드 추출',
    '사고 패턴 분석',
    '패턴 인사이트 생성',
    '초기 Seed 생성',
  ];

  // =========================
  // Analysis Result Getters
  // =========================

  Map<String, dynamic> get _seedData {
    final metadata = _analysisResult['metadata'];

    if (metadata is! Map<String, dynamic>) {
      return {};
    }

    final seed = metadata['seed'];

    if (seed is! Map<String, dynamic>) {
      return {};
    }

    return seed;
  }

  Map<String, dynamic> get _identityData {
    final identity = _analysisResult['identity'];

    if (identity is! Map<String, dynamic>) {
      return {};
    }

    return identity;
  }

  String get _identityName {
    return _identityData['identity_name']
            ?.toString() ??
        '';
  }

  String get _identityDescription {
    return _identityData['description']
            ?.toString() ??
        '';
  }

  double get _dataConfidence {
    final value =
        _seedData['data_confidence'];

    if (value is num) {
      return value.toDouble();
    }

    return 0.0;
  }

  String get _seedStage {
    return _seedData['stage']
            ?.toString() ??
        'Seed';
  }

  int get _scanCount {
    final value =
        _seedData['scan_count'];

    if (value is num) {
      return value.toInt();
    }

    return 0;
  }

  @override
  void initState() {
    super.initState();

    _analysisResult = widget.analysisResult;

    _startAnalysis();
  }

  void _updateProgress({
    required int progress,
    required int step,
  }) {
    if (!mounted) return;

    setState(() {
      _progress = progress;
      _currentStep = step;
    });
  }

  Future<void> _startAnalysis() async {
    try {
      _updateProgress(
        progress: 20,
        step: 0,
      );

      await Future.delayed(
        const Duration(
          milliseconds: 600,
        ),
      );

      _updateProgress(
        progress: 40,
        step: 1,
      );

      await Future.delayed(
        const Duration(
          milliseconds: 600,
        ),
      );

      _updateProgress(
        progress: 60,
        step: 2,
      );

      _updateProgress(
        progress: 80,
        step: 3,
      );

      await Future.delayed(
        const Duration(
          milliseconds: 700,
        ),
      );

      _updateProgress(
        progress: 100,
        step: 4,
      );

      await Future.delayed(
        const Duration(
          milliseconds: 600,
        ),
      );

      if (!mounted) return;

      setState(() {
        _completed = true;
      });
    } catch (e) {
      debugPrint(
        '===== ANALYSIS ERROR =====',
      );

      debugPrint(
        e.toString(),
      );

      if (!mounted) return;

      _showError();
    }
  }

  void _showError() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return AlertDialog(
          title: const Text(
            '분석에 실패했습니다',
          ),
          content: const Text(
            '사고 패턴 분석 중 문제가 발생했습니다.\n잠시 후 다시 시도해주세요.',
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: const Text(
                '닫기',
              ),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context);

                _startAnalysis();
              },
              child: const Text(
                '다시 시도',
              ),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(
    BuildContext context,
  ) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: LayoutBuilder(
          builder: (
            context,
            constraints,
          ) {
            return SingleChildScrollView(
              padding: const EdgeInsets.symmetric(
                horizontal: 24,
                vertical: 24,
              ),
              child: ConstrainedBox(
                constraints: BoxConstraints(
                  minHeight:
                      constraints.maxHeight - 48,
                ),
                child: Center(
                  child: _completed
                      ? _buildCompleted()
                      : _buildAnalyzing(),
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  Widget _buildAnalyzing() {
    return Container(
      width: double.infinity,
      constraints:
          const BoxConstraints(
        maxWidth: 380,
      ),
      padding:
          const EdgeInsets.all(28),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius:
            BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color:
                Colors.black.withValues(
              alpha: 0.05,
            ),
            blurRadius: 30,
            offset:
                const Offset(0, 10),
          ),
        ],
      ),
      child: Column(
        mainAxisSize:
            MainAxisSize.min,
        children: [
          const SizedBox(height: 10),

          _buildBrainVisual(),

          const SizedBox(height: 28),

          Text(
            '당신의 사고 패턴을\n분석하고 있습니다.',
            textAlign:
                TextAlign.center,
            style:
                Theme.of(context)
                    .textTheme
                    .headlineSmall
                    ?.copyWith(
                      fontWeight:
                          FontWeight.bold,
                      color:
                          AppColors.textPrimary,
                      height: 1.4,
                    ),
          ),

          const SizedBox(height: 14),

          Text(
            '응답 데이터를 바탕으로\n당신만의 패턴을 발견하는 중이에요.',
            textAlign:
                TextAlign.center,
            style:
                Theme.of(context)
                    .textTheme
                    .bodyMedium
                    ?.copyWith(
                      color:
                          AppColors.textSecondary,
                      height: 1.5,
                    ),
          ),

          const SizedBox(height: 28),

          _buildProgress(),

          const SizedBox(height: 28),

          ...List.generate(
            _steps.length,
            (index) =>
                _buildStep(index),
          ),

          const SizedBox(height: 24),

          _buildSecurityMessage(),
        ],
      ),
    );
  }

  Widget _buildBrainVisual() {
    return Container(
      width: 170,
      height: 150,
      decoration: BoxDecoration(
        shape:
            BoxShape.circle,
        color:
            AppColors.primary
                .withValues(alpha: 0.05),
      ),
      child: Stack(
        alignment:
            Alignment.center,
        children: [
          Container(
            width: 90,
            height: 90,
            decoration: BoxDecoration(
              shape:
                  BoxShape.circle,
              color:
                  AppColors.primary
                      .withValues(alpha: 0.1),
            ),
          ),
          Icon(
            Icons.hub_outlined,
            size: 70,
            color:
                AppColors.primary,
          ),
        ],
      ),
    );
  }

  Widget _buildProgress() {
    return Column(
      children: [
        Row(
          children: [
            Expanded(
              child:
                  ClipRRect(
                borderRadius:
                    BorderRadius.circular(
                  10,
                ),
                child:
                    LinearProgressIndicator(
                  value:
                      _progress / 100,
                  minHeight: 8,
                  backgroundColor:
                      AppColors.border,
                  valueColor:
                      AlwaysStoppedAnimation<
                          Color>(
                    AppColors.primary,
                  ),
                ),
              ),
            ),
            const SizedBox(width: 12),
            Text(
              '$_progress%',
              style:
                  Theme.of(context)
                      .textTheme
                      .bodyMedium
                      ?.copyWith(
                        fontWeight:
                            FontWeight.bold,
                        color:
                            AppColors.primary,
                      ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildStep(
    int index,
  ) {
    final isCompleted =
        index < _currentStep;

    final isCurrent =
        index == _currentStep;

    IconData icon;

    Color color;

    String status;

    if (isCompleted) {
      icon =
          Icons.check_circle;

      color =
          AppColors.primary;

      status = '완료';
    } else if (isCurrent) {
      icon =
          Icons.auto_awesome;

      color =
          AppColors.primary;

      status = '분석 중';
    } else {
      icon =
          Icons.radio_button_unchecked;

      color =
          AppColors.textSecondary
              .withValues(alpha: 0.4);

      status = '대기';
    }

    return Padding(
      padding:
          const EdgeInsets.symmetric(
        vertical: 9,
      ),
      child: Row(
        children: [
          Icon(
            icon,
            color: color,
            size: 20,
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Text(
              _steps[index],
              style:
                  Theme.of(context)
                      .textTheme
                      .bodyMedium
                      ?.copyWith(
                        fontWeight:
                            isCurrent
                                ? FontWeight.bold
                                : FontWeight.normal,
                        color:
                            AppColors.textPrimary,
                      ),
            ),
          ),
          Text(
            status,
            style:
                Theme.of(context)
                    .textTheme
                    .bodySmall
                    ?.copyWith(
                      color: color,
                    ),
          ),
        ],
      ),
    );
  }

  Widget _buildSecurityMessage() {
    return Container(
      width: double.infinity,
      padding:
          const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color:
            AppColors.primary
                .withValues(alpha: 0.04),
        borderRadius:
            BorderRadius.circular(
          14,
        ),
        border: Border.all(
          color:
              AppColors.border,
        ),
      ),
      child: Row(
        children: [
          Icon(
            Icons.shield_outlined,
            color:
                AppColors.primary,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              '모든 분석은 안전하게 처리되며\n당신의 데이터는 오직 당신을 위해 사용됩니다.',
              style:
                  Theme.of(context)
                      .textTheme
                      .bodySmall
                      ?.copyWith(
                        color:
                            AppColors.textSecondary,
                        height: 1.5,
                      ),
            ),
          ),
        ],
      ),
    );
  }

  // =========================
  // Analysis Completed
  // =========================

  Widget _buildCompleted() {
    return Container(
      width: double.infinity,
      constraints:
          const BoxConstraints(
        maxWidth: 380,
      ),
      padding:
          const EdgeInsets.all(28),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius:
            BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color:
                Colors.black.withValues(
              alpha: 0.05,
            ),
            blurRadius: 30,
            offset:
                const Offset(0, 10),
          ),
        ],
      ),
      child: Column(
        mainAxisSize:
            MainAxisSize.min,
        children: [
          _buildSeedVisual(),

          const SizedBox(height: 28),

          Text(
            _identityName.isNotEmpty
                ? '$_identityName Seed 생성 완료!'
                : '초기 Seed 생성 완료!',
            textAlign:
                TextAlign.center,
            style:
                Theme.of(context)
                    .textTheme
                    .headlineSmall
                    ?.copyWith(
                      fontWeight:
                          FontWeight.bold,
                      color:
                          AppColors.textPrimary,
                    ),
          ),

          const SizedBox(height: 14),

          Text(
            _identityDescription.isNotEmpty
                ? _identityDescription
                : '당신만의 MindFrame OS의\n초기 Seed가 생성되었습니다.\n더 많은 데이터를 축적할수록\n더 정확한 분석을 제공할 수 있어요.',
            textAlign:
                TextAlign.center,
            style:
                Theme.of(context)
                    .textTheme
                    .bodyMedium
                    ?.copyWith(
                      color:
                          AppColors.textSecondary,
                      height: 1.6,
                    ),
          ),

          const SizedBox(height: 28),

          _buildReliabilityCard(
            confidence:
                _dataConfidence,
          ),

          const SizedBox(height: 20),

          SizedBox(
            width: double.infinity,
            height: 54,
            child: ElevatedButton(
              onPressed: () {
                ref.invalidate(dashboardProvider);
                ref.invalidate(currentUserProvider);

                context.go(
                  RouteNames.dashboard,
                );
              },
              style:
                  ElevatedButton.styleFrom(
                backgroundColor:
                    AppColors.primary,
                foregroundColor:
                    Colors.white,
                shape:
                    RoundedRectangleBorder(
                  borderRadius:
                      BorderRadius.circular(
                    14,
                  ),
                ),
              ),
              child: const Text(
                'Dashboard로 이동  →',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight:
                      FontWeight.bold,
                ),
              ),
            ),
          ),

          const SizedBox(height: 16),

          Text(
            '현재 $_seedStage 단계 · 누적 $_scanCount회 분석',
            style:
                Theme.of(context)
                    .textTheme
                    .bodySmall
                    ?.copyWith(
                      color:
                          AppColors.textSecondary,
                    ),
          ),
        ],
      ),
    );
  }

  Widget _buildSeedVisual() {
    return Container(
      width: 170,
      height: 150,
      decoration: BoxDecoration(
        shape:
            BoxShape.circle,
        color:
            AppColors.primary
                .withValues(alpha: 0.06),
      ),
      child: Center(
        child: Icon(
          Icons.energy_savings_leaf,
          size: 70,
          color:
              AppColors.primary,
        ),
      ),
    );
  }

  Widget _buildReliabilityCard({
    required double confidence,
  }) {
    final normalizedConfidence =
        (confidence / 100)
            .clamp(0.0, 1.0);

    final confidenceText =
        '${confidence.round()}%';

    return Container(
      width: double.infinity,
      padding:
          const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color:
            AppColors.background,
        borderRadius:
            BorderRadius.circular(
          16,
        ),
        border: Border.all(
          color:
              AppColors.border,
        ),
      ),
      child: Row(
        children: [
          SizedBox(
            width: 90,
            height: 90,
            child: Stack(
              alignment:
                  Alignment.center,
              children: [
                SizedBox(
                  width: 80,
                  height: 80,
                  child:
                      CircularProgressIndicator(
                    value:
                        normalizedConfidence,
                    strokeWidth: 8,
                    backgroundColor:
                        AppColors.border,
                    valueColor:
                        AlwaysStoppedAnimation<
                            Color>(
                      AppColors.primary,
                    ),
                  ),
                ),
                Text(
                  confidenceText,
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight:
                        FontWeight.bold,
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
                Text(
                  '현재 $_seedStage 단계입니다.',
                  style: const TextStyle(
                    fontWeight:
                        FontWeight.w600,
                  ),
                ),

                const SizedBox(height: 6),

                Text(
                  '현재 분석 데이터 신뢰도는 '
                  '${confidence.round()}%입니다.\n'
                  '데이터가 축적될수록 더 정확한 분석을 제공합니다.',
                  style:
                      Theme.of(context)
                          .textTheme
                          .bodySmall
                          ?.copyWith(
                            color:
                                AppColors.textSecondary,
                            height: 1.4,
                          ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}