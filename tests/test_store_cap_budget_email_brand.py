import os

import pytest

from finance_sentiment.brand_check import BLOCKED_HASHES, check_text
from finance_sentiment.budget import Budget, NegativeCostError, validate_cost
from finance_sentiment.email_channel import EmailChannel, SendRefusedInCI
from finance_sentiment.store import (
    RowCapExceeded, fetch_capped, guarded_connection,
)


# --- Row cap ---

def test_row_cap_returns_rows_within_cap():
    conn = guarded_connection()
    cursor = conn.execute("SELECT id FROM v_documents")
    assert fetch_capped(cursor, 10) == []


def test_row_cap_raises_when_result_exceeds_cap():
    conn = guarded_connection()
    # Seed via a second, unguarded connection is not possible on
    # :memory:, so exercise fetch_capped with a plain cursor instead:
    import sqlite3
    raw = sqlite3.connect(":memory:")
    raw.execute("CREATE TABLE t (x INTEGER)")
    raw.executemany("INSERT INTO t VALUES (?)", [(1,), (2,), (3,)])
    cursor = raw.execute("SELECT x FROM t")
    with pytest.raises(RowCapExceeded):
        fetch_capped(cursor, 2)


def test_row_cap_rejects_negative_cap():
    import sqlite3
    raw = sqlite3.connect(":memory:")
    raw.execute("CREATE TABLE t (x INTEGER)")
    cursor = raw.execute("SELECT x FROM t")
    with pytest.raises(ValueError):
        fetch_capped(cursor, -1)


# --- Negative cost ---

def test_negative_cost_rejected_not_clamped():
    with pytest.raises(NegativeCostError):
        validate_cost(-5.0)


def test_budget_rejects_negative_add_and_limit():
    with pytest.raises(NegativeCostError):
        Budget(-100.0)
    budget = Budget(100.0)
    with pytest.raises(NegativeCostError):
        budget.add(-1.0)
    assert budget.spent == 0.0


def test_budget_tracks_spend_and_remaining():
    budget = Budget(100.0)
    budget.add(30.0)
    assert budget.remaining() == 70.0
    assert budget.over_budget() is False


# --- Email channel ---

def test_email_channel_dry_run_by_default_sends_nothing():
    channel = EmailChannel()
    result = channel.send("a@b.com", "Signal ready", "Body text")
    assert result.sent is False and result.dry_run is True
    assert channel.sent_log == []


def test_email_channel_refused_in_ci_even_when_opted_in(monkeypatch):
    monkeypatch.setenv("CI", "true")
    channel = EmailChannel(dry_run=False)
    with pytest.raises(SendRefusedInCI):
        channel.send("a@b.com", "Signal ready", "Body text")


def test_email_channel_opt_in_records_simulated_send(monkeypatch):
    monkeypatch.delenv("CI", raising=False)
    channel = EmailChannel(dry_run=False)
    result = channel.send("a@b.com", "Signal ready", "Body text")
    assert result.sent is True and len(channel.sent_log) == 1


# --- Brand blocklist ---

def test_brand_blocklist_is_non_empty():
    assert len(BLOCKED_HASHES) >= 1


def test_brand_check_flags_blocked_phrase_and_clears_clean_text():
    # Phrase built in reverse order so this test file itself never
    # contains the blocked phrase in reading order.
    parts = ["university", "hopkins", "johns"]
    phrase = " ".join(reversed(parts))
    assert len(check_text(phrase)) >= 1
    assert check_text("Revenue grew strongly and demand remained robust.") == []
