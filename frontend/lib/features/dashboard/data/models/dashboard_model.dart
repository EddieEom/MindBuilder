class DashboardModel {
  final HumanOsSummary? humanOs;
  final InsightSummary? insight;
  final NextActionSummary? nextAction;
  final List<RecentChange> recentChanges;
  final List<RecentArchive> recentArchives;

  const DashboardModel({
    required this.humanOs,
    required this.insight,
    required this.nextAction,
    required this.recentChanges,
    required this.recentArchives,
  });

  factory DashboardModel.fromJson(Map<String, dynamic> json) {
    return DashboardModel(
      humanOs: json['human_os'] != null
          ? HumanOsSummary.fromJson(
              json['human_os'] as Map<String, dynamic>,
            )
          : null,
      insight: json['insight'] != null
          ? InsightSummary.fromJson(
              json['insight'] as Map<String, dynamic>,
            )
          : null,
      nextAction: json['next_action'] != null
          ? NextActionSummary.fromJson(
              json['next_action'] as Map<String, dynamic>,
            )
          : null,
      recentChanges: (json['recent_changes'] as List<dynamic>? ?? [])
          .map(
            (item) => RecentChange.fromJson(
              item as Map<String, dynamic>,
            ),
          )
          .toList(),
      recentArchives: (json['recent_archives'] as List<dynamic>? ?? [])
          .map(
            (item) => RecentArchive.fromJson(
              item as Map<String, dynamic>,
            ),
          )
          .toList(),
    );
  }
}

class HumanOsSummary {
  final String? stage;
  final double? confidence;
  final String? version;

  const HumanOsSummary({
    required this.stage,
    required this.confidence,
    required this.version,
  });

  factory HumanOsSummary.fromJson(Map<String, dynamic> json) {
    return HumanOsSummary(
      stage: json['stage'] as String?,
      confidence: (json['confidence'] as num?)?.toDouble(),
      version: json['version'] as String?,
    );
  }
}

class InsightSummary {
  final String? title;
  final String? content;

  const InsightSummary({
    required this.title,
    required this.content,
  });

  factory InsightSummary.fromJson(Map<String, dynamic> json) {
    return InsightSummary(
      title: json['title'] as String?,
      content: json['content'] as String?,
    );
  }

  bool get isEmpty {
    return (title == null || title!.trim().isEmpty) &&
        (content == null || content!.trim().isEmpty);
  }
}

class NextActionSummary {
  final String? title;
  final String? actionType;
  final String? actionUrl;

  const NextActionSummary({
    required this.title,
    required this.actionType,
    required this.actionUrl,
  });

  factory NextActionSummary.fromJson(Map<String, dynamic> json) {
    return NextActionSummary(
      title: json['title'] as String?,
      actionType: json['action_type'] as String?,
      actionUrl: json['action_url'] as String?,
    );
  }
}

class RecentChange {
  final String? metric;
  final double? value;
  final double? change;

  const RecentChange({
    required this.metric,
    required this.value,
    required this.change,
  });

  factory RecentChange.fromJson(Map<String, dynamic> json) {
    return RecentChange(
      metric: json['metric'] as String?,
      value: (json['value'] as num?)?.toDouble(),
      change: (json['change'] as num?)?.toDouble(),
    );
  }
}

class RecentArchive {
  final String? eventType;
  final String? title;
  final String? summary;
  final DateTime? createdAt;

  const RecentArchive({
    required this.eventType,
    required this.title,
    required this.summary,
    required this.createdAt,
  });

  factory RecentArchive.fromJson(Map<String, dynamic> json) {
    return RecentArchive(
      eventType: json['event_type'] as String?,
      title: json['title'] as String?,
      summary: json['summary'] as String?,
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'] as String)
          : null,
    );
  }
}