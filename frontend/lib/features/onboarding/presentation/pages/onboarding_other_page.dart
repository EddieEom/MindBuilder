import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

class OnboardingOtherPage extends StatefulWidget {
  const OnboardingOtherPage({
    super.key,
    required this.questionId,
    required this.optionId,
    required this.questionType,
    required this.maxPoint,
    this.initialPoint,
    this.initialText,
  });

  final int questionId;
  final int optionId;
  final String questionType;

  final int? initialPoint;
  final String? initialText;
  final int maxPoint;

  @override
  State<OnboardingOtherPage> createState() =>
      _OnboardingOtherPageState();
}

class _OnboardingOtherPageState
    extends State<OnboardingOtherPage> {
  late final TextEditingController _otherController;

  int _point = 0;

  bool get _isPointQuestion =>
      widget.questionType == 'POINT';

  @override
  void initState() {
    super.initState();

    _otherController =
        TextEditingController(
      text: widget.initialText ?? '',
    );

    _point = widget.initialPoint ?? 0;
  }

  @override
  void dispose() {
    _otherController.dispose();

    super.dispose();
  }

  void _changePoint(
    int change,
  ) {
    setState(() {
      final nextPoint =
          _point + change;

      if (nextPoint < 0) {
        _point = 0;
        return;
      }

      if (nextPoint > widget.maxPoint) {
        _point = widget.maxPoint;
        return;
      }

      _point = nextPoint;
    });
  }

  void _complete() {
    final otherText =
        _otherController.text.trim();

    if (otherText.isEmpty) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            '기타 내용을 입력해주세요.',
          ),
        ),
      );

      return;
    }

    if (_isPointQuestion &&
        _point <= 0) {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            '포인트를 입력해주세요.',
          ),
        ),
      );

      return;
    }

    Navigator.pop(
      context,
      {
        'question_id': widget.questionId,
        'option_id': widget.optionId,
        'point_value':
            _isPointQuestion
                ? _point
                : null,
        'detail_text': otherText,
      },
    );
  }

  @override
  Widget build(
    BuildContext context,
  ) {
    return Scaffold(
      backgroundColor:
          AppColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(
            horizontal: 24,
            vertical: 20,
          ),
          child: Column(
            crossAxisAlignment:
                CrossAxisAlignment.start,
            children: [
              IconButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                icon: const Icon(
                  Icons.arrow_back,
                ),
              ),

              const SizedBox(height: 20),

              Text(
                '기타 내용을\n직접 입력해주세요.',
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

              Text(
                '질문에 포함되지 않은 내용이 있다면\n직접 입력할 수 있습니다.',
                style: Theme.of(context)
                    .textTheme
                    .bodyMedium
                    ?.copyWith(
                      color:
                          AppColors.textSecondary,
                      height: 1.5,
                    ),
              ),

              const SizedBox(height: 36),

              Text(
                '기타 입력',
                style: Theme.of(context)
                    .textTheme
                    .titleMedium
                    ?.copyWith(
                      fontWeight:
                          FontWeight.w600,
                    ),
              ),

              const SizedBox(height: 10),

              TextField(
                controller:
                    _otherController,
                maxLines: 4,
                maxLength: 300,
                decoration: InputDecoration(
                  hintText:
                      '직접 입력해주세요.',
                  filled: true,
                  fillColor:
                      Colors.white,
                  border:
                      OutlineInputBorder(
                    borderRadius:
                        BorderRadius.circular(
                      14,
                    ),
                    borderSide:
                        BorderSide(
                      color:
                          AppColors.border,
                    ),
                  ),
                  enabledBorder:
                      OutlineInputBorder(
                    borderRadius:
                        BorderRadius.circular(
                      14,
                    ),
                    borderSide:
                        BorderSide(
                      color:
                          AppColors.border,
                    ),
                  ),
                  focusedBorder:
                      OutlineInputBorder(
                    borderRadius:
                        BorderRadius.circular(
                      14,
                    ),
                    borderSide:
                        BorderSide(
                      color:
                          AppColors.primary,
                      width: 1.5,
                    ),
                  ),
                ),
              ),

              if (_isPointQuestion) ...[
                const SizedBox(height: 28),

                Text(
                  '이 항목에 얼마나 많은 에너지를 사용하나요?',
                  style: Theme.of(context)
                      .textTheme
                      .titleMedium
                      ?.copyWith(
                        fontWeight:
                            FontWeight.w600,
                      ),
                ),

                const SizedBox(height: 8),

                Text(
                  '현재 삶에서 차지하는 비중을 포인트로 표현해주세요.',
                  style: Theme.of(context)
                      .textTheme
                      .bodyMedium
                      ?.copyWith(
                        color:
                            AppColors.textSecondary,
                      ),
                ),

                const SizedBox(height: 20),

                Container(
                  width: double.infinity,
                  padding:
                      const EdgeInsets.symmetric(
                    horizontal: 20,
                    vertical: 18,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.white,
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
                    mainAxisAlignment:
                        MainAxisAlignment
                            .spaceBetween,
                    children: [
                      IconButton(
                        onPressed:
                            _point > 0
                                ? () {
                                    _changePoint(
                                      -10,
                                    );
                                  }
                                : null,
                        icon: const Icon(
                          Icons
                              .remove_circle_outline,
                        ),
                      ),

                      Column(
                        children: [
                          Text(
                            '$_point',
                            style:
                                Theme.of(context)
                                    .textTheme
                                    .headlineMedium
                                    ?.copyWith(
                                      fontWeight:
                                          FontWeight
                                              .bold,
                                      color:
                                          AppColors
                                              .primary,
                                    ),
                          ),

                          Text(
                            '포인트',
                            style:
                                Theme.of(context)
                                    .textTheme
                                    .bodySmall
                                    ?.copyWith(
                                      color:
                                          AppColors
                                              .textSecondary,
                                    ),
                          ),
                        ],
                      ),

                      IconButton(
                        onPressed:
                          _point < widget.maxPoint
                              ? () {
                                  _changePoint(
                                    10,
                                  );
                                }
                              : null,
                        icon: const Icon(
                          Icons
                              .add_circle_outline,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
              const SizedBox(height: 40),
              SizedBox(
                width: double.infinity,
                height: 56,
                child: ElevatedButton(
                  onPressed: _complete,
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
                    '완료',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight:
                          FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}