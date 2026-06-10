from decimal import Decimal

from app.services.fraud_engine import FraudDetectionEngine


def test_high_amount_scores_as_fraudulent():
    result = FraudDetectionEngine().score(Decimal("12000000"), [], 0, None)
    assert result.level == "HIGH"
    assert result.classification == "Fraudulent"
    assert result.score >= 70


def test_low_amount_scores_as_legitimate():
    result = FraudDetectionEngine().score(Decimal("100000"), [], 0, None)
    assert result.level == "LOW"
    assert result.classification == "Legitimate"


def test_frequency_and_geography_raise_risk():
    result = FraudDetectionEngine().score(Decimal("1000000"), [Decimal("900000"), Decimal("950000"), Decimal("910000")], 9, "Unknown")
    assert result.level in {"MEDIUM", "HIGH"}
    assert "suspicious frequency" in result.reasons
    assert "geographic anomaly" in result.reasons
