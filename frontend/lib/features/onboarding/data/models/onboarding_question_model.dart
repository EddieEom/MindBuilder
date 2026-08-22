class OnboardingQuestionOption {
  final int optionId;
  final String optionText;
  final String optionValue;
  final int displayOrder;

  const OnboardingQuestionOption({
    required this.optionId,
    required this.optionText,
    required this.optionValue,
    required this.displayOrder,
  });

  factory OnboardingQuestionOption.fromJson(
    Map<String, dynamic> json,
  ) {
    return OnboardingQuestionOption(
      optionId: json['option_id'] as int,
      optionText: json['option_text'] as String,
      optionValue: json['option_value'] as String,
      displayOrder: json['display_order'] as int,
    );
  }
}


class OnboardingQuestion {
  final int questionId;
  final String questionCode;
  final String title;
  final String description;
  final String questionType;
  final int displayOrder;

  final List<OnboardingQuestionOption> options;

  const OnboardingQuestion({
    required this.questionId,
    required this.questionCode,
    required this.title,
    required this.description,
    required this.questionType,
    required this.displayOrder,
    required this.options,
  });

  factory OnboardingQuestion.fromJson(
    Map<String, dynamic> json,
  ) {
    return OnboardingQuestion(
      questionId: json['question_id'] as int,
      questionCode: json['question_code'] as String,
      title: json['title'] as String,
      description: json['description'] as String,
      questionType: json['question_type'] as String,
      displayOrder: json['display_order'] as int,

      options: (json['options'] as List<dynamic>)
          .map(
            (option) =>
                OnboardingQuestionOption.fromJson(
              option as Map<String, dynamic>,
            ),
          )
          .toList(),
    );
  }
}


class OnboardingQuestionSet {
  final int setId;
  final String setName;
  final String description;
  final String targetStage;

  final List<OnboardingQuestion> questions;

  const OnboardingQuestionSet({
    required this.setId,
    required this.setName,
    required this.description,
    required this.targetStage,
    required this.questions,
  });

  factory OnboardingQuestionSet.fromJson(
    Map<String, dynamic> json,
  ) {
    return OnboardingQuestionSet(
      setId: json['set_id'] as int,
      setName: json['set_name'] as String,
      description: json['description'] as String,
      targetStage: json['target_stage'] as String,

      questions: (json['questions'] as List<dynamic>)
          .map(
            (question) =>
                OnboardingQuestion.fromJson(
              question as Map<String, dynamic>,
            ),
          )
          .toList(),
    );
  }
}