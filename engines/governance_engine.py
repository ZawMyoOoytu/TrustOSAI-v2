class GovernanceEngine:

    def evaluate(
        self,
        trust,
        risk,
        policy,
        conflict
    ):

        if conflict:
            return "REVIEW"

        if policy == "BLOCK":
            return "BLOCK"

        if trust >= 0.75 and risk <= 0.50:
            return "ALLOW"

        return "REVIEW"