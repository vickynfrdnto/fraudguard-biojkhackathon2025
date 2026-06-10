from dataclasses import dataclass
from decimal import Decimal
from statistics import mean, pstdev


@dataclass
class RiskResult:
    score: int
    level: str
    classification: str
    reasons: list[str]


class FraudDetectionEngine:
    high_risk_countries = {"Unknown", "HighRisk"}

    def score(self, amount: Decimal, history: list[Decimal] | None = None, frequency_24h: int = 0, country: str | None = None) -> RiskResult:
        history = history or []
        score = 0
        reasons: list[str] = []
        numeric_amount = float(amount)

        if numeric_amount >= 10_000_000:
            score += 70
            reasons.append("abnormal transaction amount")
        elif numeric_amount >= 5_000_000:
            score += 25
            reasons.append("elevated transaction amount")

        if len(history) >= 3:
            avg = mean(float(item) for item in history)
            deviation = pstdev(float(item) for item in history) or 1
            if numeric_amount > avg + (2 * deviation):
                score += 25
                reasons.append("unusual activity against account history")

        if frequency_24h >= 8:
            score += 25
            reasons.append("suspicious frequency")
        elif frequency_24h >= 4:
            score += 10
            reasons.append("increased transaction frequency")

        if country in self.high_risk_countries:
            score += 20
            reasons.append("geographic anomaly")

        score = min(score, 100)
        if score >= 70:
            return RiskResult(score, "HIGH", "Fraudulent", reasons or ["high composite risk"])
        if score >= 35:
            return RiskResult(score, "MEDIUM", "Suspicious", reasons or ["medium composite risk"])
        return RiskResult(score, "LOW", "Legitimate", reasons or ["within normal risk range"])
