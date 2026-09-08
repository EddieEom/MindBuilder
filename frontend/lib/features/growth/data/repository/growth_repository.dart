import '../datasource/growth_remote_datasource.dart';
import '../models/growth_model.dart';

class GrowthRepository {
  Future<void> submitFeedback(int analysisId, int rating) =>
      datasource.submitFeedback(analysisId, rating);
  Future<void> createAction(GrowthRecommendation recommendation) =>
      datasource.createAction(
        recommendation.recommendationId!,
        recommendation.title,
        recommendation.description,
      );

  final GrowthRemoteDataSource datasource;

  GrowthRepository(this.datasource);

  Future<GrowthModel> getCurrentGrowth() async {
    final json = await datasource.getCurrentGrowth();

    return GrowthModel.fromJson(json);
  }
}
