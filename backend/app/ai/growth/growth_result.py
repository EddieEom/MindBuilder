class GrowthResult:

    def __init__(self):

        # ==========================================
        # Growth
        # ==========================================

        self.unlearning = None
        self.relearning = None
        self.newlearning = None

        # ==========================================
        # AI
        # ==========================================

        self.explanations = []

        # ==========================================
        # Recommendation
        # ==========================================

        self.recommendations = []

        # ==========================================
        # Feedback
        # ==========================================

        self.feedback = {}

        # ==========================================
        # Metadata
        # ==========================================

        self.metadata = {}

        # ==========================================
        # Warnings
        # ==========================================
        
        self.warnings = []

    # ======================================================
    # Growth
    # ======================================================

    def set_unlearning(
        self,
        item: dict,
    ) -> None:

        self.unlearning = item

    def set_relearning(
        self,
        item: dict,
    ) -> None:

        self.relearning = item

    def set_newlearning(
        self,
        item: dict,
    ) -> None:

        self.newlearning = item

    # ======================================================
    # Explanation
    # ======================================================

    def add_explanation(
        self,
        explanation: dict,
    ) -> None:

        self.explanations.append(
            explanation,
        )

    # ======================================================
    # Recommendation
    # ======================================================

    def add_recommendation(
        self,
        recommendation: dict,
    ) -> None:

        self.recommendations.append(
            recommendation,
        )

    # ======================================================
    # Feedback
    # ======================================================

    def set_feedback(
        self,
        feedback: dict,
    ) -> None:

        self.feedback = feedback

    # ======================================================
    # Metadata
    # ======================================================

    def set_metadata(
        self,
        key: str,
        value,
    ) -> None:

        self.metadata[key] = value


    # ==========================================
    # Warnings
    # ==========================================
    
    def add_warning(
        self,
        warning: str,
    ) -> None:

        self.warnings.append(warning)
