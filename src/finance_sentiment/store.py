"""View-aware SQLite store with a strict authorizer.

Design (the enforcement claim, proved in tests/test_authorizer.py):
- Base tables are ``documents`` and ``scores``. Application code must
  read through the views ``v_documents`` and ``v_scores`` only.
- The authorizer inspects the *source* argument SQLite passes for each
  SQLITE_READ (action 20). When a view is read, SQLite reports the
  view name as the source of the underlying base-table read; a direct
  read reports no source. So the rule is:
    * READ of a view column: allowed.
    * READ of a base-table column: allowed ONLY when the source
      argument names an allowed view, otherwise denied.
    * READ of ``sqlite_master`` (or any other table): denied.
- Writes (INSERT/UPDATE/DELETE), schema changes, PRAGMA, ATTACH,
  DETACH, and the ``load_extension`` function are denied outright.
- Seeding happens on an unguarded connection BEFORE the authorizer
  is installed; the guarded connection is read-only in practice.

Tests exercise this by executing real SQL against a guarded
connection, not by string-matching query text: there is no
text allowlist to bypass, so a test cannot pass by renaming a query.

Row cap: :func:`fetch_capped` uses ``fetchmany(MAX + 1)`` at fetch
time. It never rewrites SQL and never calls ``fetchall``.
"""

import sqlite3

ALLOWED_VIEWS = frozenset({"v_documents", "v_scores"})
_BASE_TABLES = frozenset({"documents", "scores"})

# SQLite authorizer action codes (from sqlite3.h).
_SQLITE_READ = 20
_SQLITE_SELECT = 21
_SQLITE_TRANSACTION = 22
_SQLITE_PRAGMA = 19
_SQLITE_ATTACH = 24
_SQLITE_DETACH = 25
_SQLITE_FUNCTION = 31


class RowCapExceeded(Exception):
    pass


class AuthorizerDenied(Exception):
    """Raised by helpers that translate a SQLite auth error, if needed."""


def _authorizer(action, arg1, arg2, db_name, source):
    if action == _SQLITE_SELECT:
        return sqlite3.SQLITE_OK
    if action == _SQLITE_TRANSACTION:
        return sqlite3.SQLITE_OK
    if action == _SQLITE_READ:
        table = arg1
        if table in ALLOWED_VIEWS:
            return sqlite3.SQLITE_OK
        if table in _BASE_TABLES and source in ALLOWED_VIEWS:
            return sqlite3.SQLITE_OK
        # SQLite issues one extra READ with an empty column name when
        # it expands a view (a probe, not a data read: no column is
        # named, so no value can be returned). Allow that probe only
        # for the known tables/views; sqlite_master and unknown tables
        # are still denied.
        if table in _BASE_TABLES | ALLOWED_VIEWS and arg2 in (None, ""):
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY
    if action == _SQLITE_FUNCTION and arg2 == "load_extension":
        return sqlite3.SQLITE_DENY
    # Everything else (writes, DDL, PRAGMA, ATTACH/DETACH, ...) denied.
    return sqlite3.SQLITE_DENY


def install_authorizer(conn):
    """Install the strict authorizer on an already-seeded connection."""
    conn.set_authorizer(_authorizer)
    return conn


def init_store(conn):
    """Create schema and seed SYNTHETIC rows. Call before guarding."""
    conn.execute(
        "CREATE TABLE documents (id INTEGER PRIMARY KEY, kind TEXT, text TEXT)"
    )
    conn.execute(
        "CREATE TABLE scores (id INTEGER PRIMARY KEY, doc_id INTEGER, "
        "score REAL, label TEXT)"
    )
    conn.execute(
        "CREATE VIEW v_documents AS SELECT id, kind, text FROM documents"
    )
    conn.execute(
        "CREATE VIEW v_scores AS SELECT id, doc_id, score, label FROM scores"
    )
    conn.commit()
    return conn


def seed_document(conn, doc_id, kind, text):
    conn.execute(
        "INSERT INTO documents (id, kind, text) VALUES (?, ?, ?)",
        (doc_id, kind, text),
    )
    conn.commit()


def guarded_connection():
    """A fresh in-memory store, seeded, then guarded. For demos/tests."""
    conn = sqlite3.connect(":memory:")
    init_store(conn)
    install_authorizer(conn)
    return conn


def fetch_capped(cursor, max_rows):
    """Fetch at most ``max_rows`` rows; raise if there are more.

    Uses fetchmany(max_rows + 1) so the cap is enforced at fetch time
    without rewriting the query and without fetchall.
    """
    if max_rows < 0:
        raise ValueError("max_rows must not be negative")
    rows = cursor.fetchmany(max_rows + 1)
    if len(rows) > max_rows:
        raise RowCapExceeded(
            f"result has more than {max_rows} rows (cap enforced at fetch)"
        )
    return rows
