class GrowthModel {
  final List<GrowthExplanation> explanations;
  final List<GrowthAction> actions;
  final List<GrowthItem> items;
  final List<GrowthRecommendation> recommendations;
  final GrowthFeedback? feedback;
  final GrowthMetadata metadata;

  const GrowthModel({
    this.explanations = const [],
    this.actions = const [],
    required this.items,
    required this.recommendations,
    required this.feedback,
    required this.metadata,
  });

  factory GrowthModel.fromJson(Map<String, dynamic> json) {
    return GrowthModel(
      explanations: (json['explanations'] as List? ?? [])
          .map(
            (e) =>
                GrowthExplanation(e['title'] as String, e['content'] as String),
          )
          .toList(),
      actions: (json['actions'] as List? ?? [])
          .map(
            (e) => GrowthAction(
              e['action_id'] as int,
              e['recommendation_id'] as int,
              e['status'] as String,
            ),
          )
          .toList(),
      items: (json['items'] as List<dynamic>? ?? [])
          .map((e) => GrowthItem.fromJson(e as Map<String, dynamic>))
          .toList(),

      recommendations: (json['recommendations'] as List<dynamic>? ?? [])
          .map((e) => GrowthRecommendation.fromJson(e as Map<String, dynamic>))
          .toList(),

      feedback: json['feedback'] != null
          ? GrowthFeedback.fromJson(json['feedback'])
          : null,

      metadata: GrowthMetadata.fromJson(json['metadata']),
    );
  }
}

class GrowthItem {
  final String type;
  final String title;
  final String content;
  final int priority;

  const GrowthItem({
    required this.type,
    required this.title,
    required this.content,
    required this.priority,
  });

  factory GrowthItem.fromJson(Map<String, dynamic> json) {
    return GrowthItem(
      type: json['type'] ?? '',
      title: json['title'] ?? '',
      content: json['content'] ?? '',
      priority: json['priority'] ?? 0,
    );
  }
}

class GrowthRecommendation {
  final int? recommendationId;
  final String title;
  final String description;
  final int priority;

  const GrowthRecommendation({
    this.recommendationId,
    required this.title,
    required this.description,
    required this.priority,
  });

  factory GrowthRecommendation.fromJson(Map<String, dynamic> json) {
    return GrowthRecommendation(
      recommendationId: json['recommendation_id'] as int?,
      title: json['title'] ?? '',
      description: json['description'] ?? '',
      priority: json['priority'] ?? 0,
    );
  }
}

class GrowthFeedback {
  final int rating;
  final String comment;

  const GrowthFeedback({required this.rating, required this.comment});

  factory GrowthFeedback.fromJson(Map<String, dynamic> json) {
    return GrowthFeedback(
      rating: json['rating'] ?? 0,
      comment: json['comment'] ?? '',
    );
  }
}

class GrowthMetadata {
  final int growthAnalysisId;
  final String analysisVersion;
  final String llmModel;
  final double confidence;
  final DateTime? createdAt;

  const GrowthMetadata({
    required this.growthAnalysisId,
    required this.analysisVersion,
    required this.llmModel,
    required this.confidence,
    required this.createdAt,
  });

  factory GrowthMetadata.fromJson(Map<String, dynamic> json) {
    return GrowthMetadata(
      growthAnalysisId: json['growth_analysis_id'] ?? 0,

      analysisVersion: json['analysis_version'] ?? '',

      llmModel: json['llm_model'] ?? '',

      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,

      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'])
          : null,
    );
  }
}

class GrowthExplanation {
  const GrowthExplanation(this.title, this.content);
  final String title;
  final String content;
}

class GrowthAction {
  const GrowthAction(this.id, this.recommendationId, this.status);
  final int id;
  final int recommendationId;
  final String status;
}
