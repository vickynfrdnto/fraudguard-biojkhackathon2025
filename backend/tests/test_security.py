from datetime import timedelta

import pytest

from app.core.security import create_token, decode_token, sanitize


def test_token_roundtrip():
    token = create_token("123", "access", timedelta(minutes=1))
    assert decode_token(token, "access") == "123"


def test_token_rejects_wrong_type():
    token = create_token("123", "refresh", timedelta(minutes=1))
    with pytest.raises(ValueError):
        decode_token(token, "access")


def test_sanitize_strips_html():
    assert sanitize("<script>x</script>Jane") == "xJane"
