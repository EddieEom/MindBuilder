class IdentityResult:

    def __init__(self):

        # ==========================================
        # Identity
        # ==========================================

        self.identity_name = ""
        self.description = ""
        self.confidence = 0.0

        # ==========================================
        # Identity Score
        # ==========================================

        self.creativity_score = 0
        self.execution_score = 0
        self.uncertainty_score = 0

        # ==========================================
        # Candidate Identity Scores
        # ==========================================

        self.identity_scores = {}
        self.ranking = []
        self.primary_identity = ""
        self.secondary_identity = ""
        self.score_gap = 0.0
        self.matched_rules = []
        self.evidence = {}

        # ==========================================
        # Keywords
        # ==========================================

        self.keywords = []

        # ==========================================
        # Strength
        # ==========================================

        self.strengths = []

        # ==========================================
        # Growth Point
        # ==========================================

        self.growth_points = []

        # ==========================================
        # Metadata
        # ==========================================

        self.metadata = {}

        # ==========================================
        # Warning
        # ==========================================

        self.warnings = []

    # ======================================================
    # Identity
    # ======================================================

    def set_identity(
        self,
        identity_name: str,
        description: str,
        confidence: float,
    ) -> None:

        self.identity_name = identity_name
        self.description = description
        self.confidence = confidence

    # ======================================================
    # Score
    # ======================================================

    def set_scores(
        self,
        creativity: int,
        execution: int,
        uncertainty: int,
    ) -> None:

        self.creativity_score = creativity
        self.execution_score = execution
        self.uncertainty_score = uncertainty

    def set_identity_scores(
        self,
        identity_scores: dict,
    ) -> None:

        self.identity_scores = identity_scores

    def set_ranking(
        self,
        ranking: list,
    ) -> None:

        self.ranking = ranking

    def set_primary_identity(
        self,
        identity_name: str,
    ) -> None:

        self.primary_identity = identity_name

    def set_secondary_identity(
        self,
        identity_name: str,
    ) -> None:

        self.secondary_identity = identity_name

    def set_score_gap(
        self,
        score_gap: float,
    ) -> None:

        self.score_gap = score_gap

    # ======================================================
    # Rule Evidence
    # ======================================================

    def add_matched_rule(
        self,
        matched_rule: dict,
    ) -> None:

        self.matched_rules.append(
            matched_rule
        )

    def set_evidence(
        self,
        evidence: dict,
    ) -> None:

        self.evidence = evidence

    # ======================================================
    # Keyword
    # ======================================================

    def add_keyword(
        self,
        keyword: str,
    ) -> None:

        self.keywords.append(keyword)

    # ======================================================
    # Strength
    # ======================================================

    def add_strength(
        self,
        strength: str,
    ) -> None:

        self.strengths.append(strength)

    # ======================================================
    # Growth Point
    # ======================================================

    def add_growth_point(
        self,
        growth_point: str,
    ) -> None:

        self.growth_points.append(growth_point)

    # ======================================================
    # Metadata
    # ======================================================

    def set_metadata(
        self,
        key: str,
        value,
    ) -> None:

        self.metadata[key] = value

    # ======================================================
    # Warning
    # ======================================================

    def add_warning(
        self,
        warning: str,
    ) -> None:

        self.warnings.append(warning)
