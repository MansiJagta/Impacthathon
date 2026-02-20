class RiskScoring:

    def calculate(self, failed_checks):

        base_score = 0

        for fail in failed_checks:
            base_score += 2

        return min(base_score, 10)
