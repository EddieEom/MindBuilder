import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../data/models/onboarding_question_model.dart';
import '../../data/repositories/onboarding_repository.dart';
import 'onboarding_other_page.dart';
import '../../../analysis/presentation/pages/analysis_loading_page.dart';

class OnboardingPage extends StatefulWidget {
  const OnboardingPage({super.key});

  @override
  State<OnboardingPage> createState() =>
      _OnboardingPageState();
}

class _OnboardingPageState extends State<OnboardingPage> {
  
  final OnboardingRepository _repository = OnboardingRepository();

  bool _isLoading = true;
  bool _isAnalyzing = false;

  String? _errorMessage;

  int? _scanId;

  OnboardingQuestionSet? _questionSet;

  int _currentQuestionIndex = 0;

  bool _isOtherOption(
    OnboardingQuestionOption option,
  ) {
    return option.optionValue
        .toLowerCase()
        .contains('other');
  }
  // SINGLE 질문 답변
  final Map<int, int> _singleAnswers = {};

  // MULTI 질문 답변
  final Map<int, Set<int>> _multiAnswers = {};

  // POINT 질문 답변
  final Map<int, Map<int, int>> _pointAnswers = {};

  final Map<int, Map<String, dynamic>> _otherAnswers = {};

  @override
  void initState() {
    super.initState();

    _initializeScan();
  }

  Future<void> _initializeScan() async {
    try {
      debugPrint(
        '===== ONBOARDING SCAN START =====',
      );

      // 1. Scan 생성
      final scanId =
          await _repository.startOnboarding();

      debugPrint('Scan ID: $scanId');

      // 2. 질문 조회
      final questionSet =
          await _repository.getQuestions();

      debugPrint(
        'Questions loaded: '
        '${questionSet.questions.length}',
      );

      if (!mounted) return;

      setState(() {
        _scanId = scanId;
        _questionSet = questionSet;
        _isLoading = false;
      });
    } catch (e) {
      debugPrint(
        '===== ONBOARDING SCAN ERROR =====',
      );

      debugPrint(e.toString());

      if (!mounted) return;

      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  Future<void> _selectSingleOption(
    OnboardingQuestion question,
    OnboardingQuestionOption option,
  ) async {
    if (_isOtherOption(option)) {
      final result = await Navigator.push<
          Map<String, dynamic>
        >(
        context,
        MaterialPageRoute(
          builder: (_) => OnboardingOtherPage(
            questionId: question.questionId,
            optionId: option.optionId,
            questionType: question.questionType,
            maxPoint: 0,
            initialText:
                _otherAnswers[question.questionId]
                    ?['detail_text'],
          ),
        ),
      );

      if (result == null) return;

      setState(() {
        _singleAnswers[question.questionId] =
            option.optionId;

        _otherAnswers[question.questionId] =
            result;
      });

      return;
    }

    setState(() {
      _singleAnswers[question.questionId] =
          option.optionId;

      _otherAnswers.remove(
        question.questionId,
      );
    });
  }

  Future<void> _toggleMultiOption(
    OnboardingQuestion question,
    OnboardingQuestionOption option,
  ) async {
    final selectedOptions =
        _multiAnswers.putIfAbsent(
      question.questionId,
      () => <int>{},
    );

    // 이미 선택된 경우 → 해제
    if (selectedOptions.contains(option.optionId)) {
      setState(() {
        selectedOptions.remove(option.optionId);

        if (_isOtherOption(option)) {
          _otherAnswers.remove(
            question.questionId,
          );
        }
      });

      return;
    }

    // 최대 2개 제한
    if (selectedOptions.length >= 2) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            '최대 2개까지 선택할 수 있습니다.',
          ),
        ),
      );

      return;
    }

    // 기타 선택
    if (_isOtherOption(option)) {
      final result = await Navigator.push<
          Map<String, dynamic>
        >(
        context,
        MaterialPageRoute(
          builder: (_) => OnboardingOtherPage(
            questionId: question.questionId,
            optionId: option.optionId,
            questionType: question.questionType,
            maxPoint: 0,
            initialText:
                _otherAnswers[question.questionId]
                    ?['detail_text'],
          ),
        ),
      );

      if (result == null) return;

      setState(() {
        selectedOptions.add(option.optionId);

        _otherAnswers[question.questionId] =
            result;
      });

      return;
    }

    setState(() {
      selectedOptions.add(option.optionId);
    });
  }

  void _changePoint(
    OnboardingQuestion question,
    OnboardingQuestionOption option,
    int change,
  ) {
    setState(() {
      final pointMap =
          _pointAnswers.putIfAbsent(
        question.questionId,
        () => <int, int>{},
      );

      final currentPoint =
          pointMap[option.optionId] ?? 0;

      // 현재 전체 사용 포인트
      final totalUsed =
          pointMap.values.fold<int>(
        0,
        (sum, point) => sum + point,
      );

      // 증가
      if (change > 0) {
        if (totalUsed >= 100) {
          return;
        }

        final availablePoint =
            100 - totalUsed;

        final actualChange =
            change > availablePoint
                ? availablePoint
                : change;

        pointMap[option.optionId] =
            currentPoint + actualChange;

        return;
      }

      // 감소
      if (change < 0) {
        final nextPoint =
            currentPoint + change;

        if (nextPoint < 0) {
          pointMap[option.optionId] = 0;
        } else {
          pointMap[option.optionId] =
              nextPoint;
        }
      }
    });
  }

  int _getTotalPoint(
    OnboardingQuestion question,
  ) {
    final pointMap =
        _pointAnswers[question.questionId];

    if (pointMap == null) {
      return 0;
    }

    return pointMap.values.fold<int>(
      0,
      (sum, point) => sum + point,
    );
  }

  bool _hasAnswer(
    OnboardingQuestion question,
  ) {
    switch (question.questionType) {
      case 'SINGLE':
        return _singleAnswers.containsKey(
          question.questionId,
        );

      case 'MULTI':
        return _multiAnswers[
                question.questionId
              ]?.isNotEmpty ??
            false;

      case 'POINT':
        return _getTotalPoint(question) == 100;

      default:
        return false;
    }
  }

  List<Map<String, dynamic>> _buildAnswersPayload() {
    final List<Map<String, dynamic>> answers = [];

    // SINGLE
    _singleAnswers.forEach(
      (questionId, optionId) {
        final otherData =
            _otherAnswers[questionId];

        answers.add({
          'question_id': questionId,
          'option_id': optionId,
          'point_value': 0,
          'detail_text':
              otherData?['detail_text'],
        });
      },
    );

    // MULTI
    _multiAnswers.forEach(
      (questionId, optionIds) {
        for (final optionId in optionIds) {
          final Map<String, dynamic>? otherData =
            _otherAnswers[questionId];

        final detailText =
            otherData != null &&
                    otherData['option_id'] == optionId
                ? otherData['detail_text']
                : null;

        answers.add({
          'question_id': questionId,
          'option_id': optionId,
          'point_value': 0,
          'detail_text': detailText,
        });
        }
      },
    );

    // POINT
    _pointAnswers.forEach(
      (questionId, pointMap) {
        pointMap.forEach(
          (optionId, pointValue) {
            final Map<String, dynamic>? otherData =
              _otherAnswers[questionId];

          final detailText =
              otherData != null &&
                      otherData['option_id'] == optionId
                  ? otherData['detail_text']
                  : null;

          answers.add({
            'question_id': questionId,
            'option_id': optionId,
            'point_value': pointValue,
            'detail_text': detailText,
          });
          },
        );
      },
    );

    return answers;
  }
  
  void _nextQuestion() {
    final questionSet = _questionSet;

    if (questionSet == null) return;

    final questions =
        questionSet.questions;

    final question =
        questions[_currentQuestionIndex];

    if (!_hasAnswer(question)) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            '답변을 입력해주세요.',
          ),
        ),
      );

      return;
    }

    if (_currentQuestionIndex <
        questions.length - 1) {
      setState(() {
        _currentQuestionIndex++;
      });

      return;
    }

    _completeOnboarding();
  }

  Future<void> _completeOnboarding() async {
    if (_isAnalyzing) return;

    if (_scanId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Scan 정보를 찾을 수 없습니다.',
          ),
        ),
      );
      return;
    }

    setState(() {
      _isAnalyzing = true;
    });

    try {
      final answers = _buildAnswersPayload();

      final result =
          await _repository.submitAnswers(
        scanId: _scanId!,
        answers: answers,
      );

      if (!mounted) return;

      await Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => AnalysisLoadingPage(
            scanId: _scanId!,
            analysisResult: result,
          ),
        ),
      );

    } catch (e) {
      debugPrint(
        '===== ONBOARDING COMPLETE ERROR =====',
      );

      debugPrint(
        e.toString(),
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            '분석 중 오류가 발생했습니다.\n$e',
          ),
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          _isAnalyzing = false;
        });
      }
    }
  }

  void _previousQuestion() {
    if (_currentQuestionIndex == 0) {
      return;
    }

    setState(() {
      _currentQuestionIndex--;
    });
  }

  Widget _buildQuestionContent(
    OnboardingQuestion question,
  ) {
    switch (question.questionType) {
      case 'POINT':
        return _buildPointQuestion(
          question,
        );

      case 'MULTI':
        return _buildMultiQuestion(
          question,
        );

      case 'SINGLE':
        return _buildSingleQuestion(
          question,
        );

      default:
        return const Center(
          child: Text(
            '지원하지 않는 질문 유형입니다.',
          ),
        );
    }
  }
  
  Widget _buildSingleQuestion(
    OnboardingQuestion question,
  ) {
    final selectedOptionId =
        _singleAnswers[question.questionId];

    return ListView.separated(
      itemCount: question.options.length,
      separatorBuilder: (
        context,
        index,
      ) =>
          const SizedBox(height: 12),
      itemBuilder: (
        context,
        index,
      ) {
        final option =
            question.options[index];

        final isSelected =
            selectedOptionId ==
                option.optionId;

        return SizedBox(
          width: double.infinity,
          height: 60,
          child: OutlinedButton(
            onPressed: () {
              _selectSingleOption(
                question,
                option,
              );
            },
            style:
                OutlinedButton.styleFrom(
              alignment:
                  Alignment.centerLeft,
              padding:
                  const EdgeInsets.symmetric(
                horizontal: 20,
              ),
              backgroundColor:
                  isSelected
                      ? AppColors.primary
                          .withValues(
                          alpha: 0.08,
                        )
                      : Colors.white,
              side: BorderSide(
                color: isSelected
                    ? AppColors.primary
                    : AppColors.border,
                width:
                    isSelected ? 2 : 1,
              ),
              shape:
                  RoundedRectangleBorder(
                borderRadius:
                    BorderRadius.circular(
                  14,
                ),
              ),
            ),
            child: Row(
              children: [
                Icon(
                  isSelected
                      ? Icons.radio_button_checked
                      : Icons.radio_button_off,
                  color: isSelected
                      ? AppColors.primary
                      : AppColors.textSecondary,
                ),

                const SizedBox(width: 12),

                Expanded(
                  child: Text(
                    option.optionText,
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight:
                          isSelected
                              ? FontWeight.w600
                              : FontWeight.normal,
                      color:
                          AppColors.textPrimary,
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildMultiQuestion(
    OnboardingQuestion question,
  ) {
    final selectedOptions =
        _multiAnswers[question.questionId] ??
            <int>{};

    return ListView.separated(
      itemCount: question.options.length,
      separatorBuilder: (
        context,
        index,
      ) =>
          const SizedBox(height: 12),
      itemBuilder: (
        context,
        index,
      ) {
        final option =
            question.options[index];

        final isSelected =
            selectedOptions.contains(
          option.optionId,
        );

        return SizedBox(
          width: double.infinity,
          height: 60,
          child: OutlinedButton(
            onPressed: () {
              _toggleMultiOption(
                question,
                option,
              );
            },
            style:
                OutlinedButton.styleFrom(
              alignment:
                  Alignment.centerLeft,
              padding:
                  const EdgeInsets.symmetric(
                horizontal: 20,
              ),
              backgroundColor:
                  isSelected
                      ? AppColors.primary
                          .withValues(
                          alpha: 0.08,
                        )
                      : Colors.white,
              side: BorderSide(
                color: isSelected
                    ? AppColors.primary
                    : AppColors.border,
                width:
                    isSelected ? 2 : 1,
              ),
              shape:
                  RoundedRectangleBorder(
                borderRadius:
                    BorderRadius.circular(
                  14,
                ),
              ),
            ),
            child: Row(
              children: [
                Icon(
                  isSelected
                      ? Icons.check_box
                      : Icons.check_box_outline_blank,
                  color: isSelected
                      ? AppColors.primary
                      : AppColors.textSecondary,
                ),

                const SizedBox(width: 12),

                Expanded(
                  child: Text(
                    option.optionText,
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight:
                          isSelected
                              ? FontWeight.w600
                              : FontWeight.normal,
                      color:
                          AppColors.textPrimary,
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildPointQuestion(
    OnboardingQuestion question,
  ) {
    final pointMap =
        _pointAnswers[question.questionId] ??
            <int, int>{};

    final totalPoint =
        _getTotalPoint(question);

    final remainingPoint =
        100 - totalPoint;

    return Column(
      children: [
        Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(
            horizontal: 20,
            vertical: 16,
          ),
          decoration: BoxDecoration(
            color: AppColors.primary.withValues(
              alpha: 0.08,
            ),
            borderRadius:
                BorderRadius.circular(14),
          ),
          child: Row(
            mainAxisAlignment:
                MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                '남은 포인트',
                style: TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w600,
                ),
              ),
              Text(
                '$remainingPoint / 100',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: AppColors.primary,
                ),
              ),
            ],
          ),
        ),

        const SizedBox(height: 16),

        Expanded(
          child: ListView.separated(
            itemCount: question.options.length,
            separatorBuilder: (
              context,
              index,
            ) =>
                const SizedBox(height: 12),
            itemBuilder: (
              context,
              index,
            ) {
              final option =
                  question.options[index];

              final isOther =
                  _isOtherOption(option);

              final point =
                  pointMap[option.optionId] ?? 0;

              final maxPoint =
                  remainingPoint + point;

              return Container(
                padding:
                    const EdgeInsets.symmetric(
                  horizontal: 20,
                  vertical: 12,
                ),
                decoration: BoxDecoration(
                  color: Colors.white,
                  border: Border.all(
                    color: AppColors.border,
                  ),
                  borderRadius:
                      BorderRadius.circular(14),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: Text(
                        option.optionText,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),

                    if (isOther)
                      TextButton(
                        onPressed: () async {
                          final result =
                              await Navigator.push<Map<String, dynamic>>(
                            context,
                            MaterialPageRoute(
                              builder: (_) => OnboardingOtherPage(
                                questionId: question.questionId,
                                optionId: option.optionId,
                                questionType: question.questionType,
                                initialPoint: point,
                                maxPoint: maxPoint,
                                initialText:
                                    _otherAnswers[question.questionId]
                                        ?['detail_text'],
                              ),
                            ),
                          );

                          if (result == null) return;

                          final pointValue =
                              result['point_value'] as int;

                          setState(() {
                            _pointAnswers
                                .putIfAbsent(
                              question.questionId,
                              () => <int, int>{},
                            )[option.optionId] =
                                pointValue;

                            _otherAnswers[
                                question.questionId] = result;
                          });
                        },
                        child: Text(
                          point > 0
                              ? '$point 수정'
                              : '직접 입력',
                        ),
                      )
                    else ...[
                      IconButton(
                        onPressed: point > 0
                            ? () {
                                _changePoint(
                                  question,
                                  option,
                                  -10,
                                );
                              }
                            : null,
                        icon: const Icon(
                          Icons.remove_circle_outline,
                        ),
                      ),

                      SizedBox(
                        width: 44,
                        child: Text(
                          '$point',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: AppColors.primary,
                          ),
                        ),
                      ),

                      IconButton(
                        onPressed:
                            remainingPoint > 0
                                ? () {
                                    _changePoint(
                                      question,
                                      option,
                                      10,
                                    );
                                  }
                                : null,
                        icon: const Icon(
                          Icons.add_circle_outline,
                        ),
                      ),
                    ],
                  ],
                ),
              );
            },
          ),
        ),
      ],
    );
  }


  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        backgroundColor: AppColors.background,
        body: const Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    if (_errorMessage != null) {
      return Scaffold(
        backgroundColor: AppColors.background,
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Text(
              '질문을 불러오지 못했습니다.\n\n'
              '$_errorMessage',
              textAlign: TextAlign.center,
            ),
          ),
        ),
      );
    }

    final questionSet = _questionSet;

    if (questionSet == null ||
        questionSet.questions.isEmpty) {
      return const Scaffold(
        body: Center(
          child: Text(
            '등록된 질문이 없습니다.',
          ),
        ),
      );
    }

    final questions =
        questionSet.questions;

    final question =
        questions[_currentQuestionIndex];

    final progress =
        (_currentQuestionIndex + 1) /
            questions.length;

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: 24,
            vertical: 16,
          ),
          child: Column(
            crossAxisAlignment:
                CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  if (_currentQuestionIndex > 0)
                    IconButton(
                      onPressed:
                          _previousQuestion,
                      icon: const Icon(
                        Icons.arrow_back,
                      ),
                    ),

                  Expanded(
                    child:
                        LinearProgressIndicator(
                      value: progress,
                      borderRadius:
                          BorderRadius.circular(
                        10,
                      ),
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 32),

              Text(
                '${_currentQuestionIndex + 1}'
                ' / ${questions.length}',
                style: Theme.of(context)
                    .textTheme
                    .bodyMedium
                    ?.copyWith(
                      color:
                          AppColors.textSecondary,
                    ),
              ),

              const SizedBox(height: 16),

              // 질문 제목
              Text(
                question.title,
                style: Theme.of(context)
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

              const SizedBox(height: 12),

              // 질문 설명
              if (question.description.isNotEmpty)
                Text(
                  question.description,
                  style: Theme.of(context)
                      .textTheme
                      .bodyMedium
                      ?.copyWith(
                        color:
                            AppColors.textSecondary,
                        height: 1.5,
                      ),
                ),

              const SizedBox(height: 32),

              
                Expanded(
                  child: _buildQuestionContent(
                    question,
                  ),
                ),
              

              SizedBox(
                width: double.infinity,
                height: 56,
                child: ElevatedButton(
                  onPressed:
                  _isAnalyzing
                      ? null
                      : _nextQuestion,
                    style:
                        ElevatedButton.styleFrom(
                      backgroundColor:
                          AppColors.primary,
                    foregroundColor:
                        Colors.white,
                    shape:
                        RoundedRectangleBorder(
                      borderRadius:
                          BorderRadius.circular(14),
                    ),
                  ),
                  child: _isAnalyzing
                    ? const SizedBox(
                        width: 24,
                        height: 24,
                        child:
                            CircularProgressIndicator(
                          strokeWidth: 2,
                          color: Colors.white,
                        ),
                      )
                    : Text(
                        _currentQuestionIndex ==
                                questions.length - 1
                            ? '분석 시작하기'
                            : '다음',
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