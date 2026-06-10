from datetime import datetime, timedelta, timezone

from app.api.routes.dashboard import _legacy_status, _relative_time


def test_legacy_status_mapping():
    assert _legacy_status("Fraudulent") == "Fraud"
    assert _legacy_status("Legitimate") == "Normal"


def test_relative_time_formats_minutes():
    assert "min ago" in _relative_time(datetime.now(timezone.utc) - timedelta(minutes=5))
