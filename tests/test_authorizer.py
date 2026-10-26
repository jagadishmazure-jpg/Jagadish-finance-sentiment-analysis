"""Authorizer proof tests.

These tests execute real SQL against a guarded connection. There is
no query-text allowlist: the authorizer decision comes from SQLite's
own source argument, so renaming a query cannot bypass it. Seeding
happens before the authorizer is installed (see store.py).
"""

import sqlite3

import pytest

from finance_sentiment.store import (
    guarded_connection, init_store, install_authorizer, seed_document,
)


def _seeded_guarded():
    conn = sqlite3.connect(":memory:")
    init_store(conn)
    seed_document(conn, 1, "earnings_call", "Revenue grew strongly.")
    install_authorizer(conn)
    return conn


def test_authorizer_allows_view_read():
    conn = _seeded_guarded()
    rows = conn.execute("SELECT id, kind FROM v_documents").fetchall()
    assert rows == [(1, "earnings_call")]


def test_authorizer_denies_direct_base_table_read():
    conn = _seeded_guarded()
    with pytest.raises(sqlite3.DatabaseError):
        conn.execute("SELECT id FROM documents").fetchall()


def test_authorizer_denies_sqlite_master_read():
    conn = _seeded_guarded()
    with pytest.raises(sqlite3.DatabaseError):
        conn.execute("SELECT name FROM sqlite_master").fetchall()


def test_authorizer_denies_write_insert():
    conn = _seeded_guarded()
    with pytest.raises(sqlite3.DatabaseError):
        conn.execute("INSERT INTO documents VALUES (2, 'x', 'y')")


def test_authorizer_denies_write_update_and_delete():
    conn = _seeded_guarded()
    with pytest.raises(sqlite3.DatabaseError):
        conn.execute("UPDATE documents SET text='z' WHERE id=1")
    with pytest.raises(sqlite3.DatabaseError):
        conn.execute("DELETE FROM documents WHERE id=1")


def test_authorizer_denies_pragma():
    conn = _seeded_guarded()
    with pytest.raises(sqlite3.DatabaseError):
        conn.execute("PRAGMA foreign_keys=ON").fetchall()


def test_authorizer_denies_attach():
    conn = _seeded_guarded()
    with pytest.raises(sqlite3.DatabaseError):
        conn.execute("ATTACH ':memory:' AS other")


def test_authorizer_denies_view_read_of_scores_base_via_direct_table():
    conn = _seeded_guarded()
    with pytest.raises(sqlite3.DatabaseError):
        conn.execute("SELECT * FROM scores").fetchall()


def test_authorizer_allows_scores_view_read():
    conn = _seeded_guarded()
    rows = conn.execute("SELECT id FROM v_scores").fetchall()
    assert rows == []
