# ADR 002: View-only reads enforced by the authorizer

- **Status:** Accepted
- **Context:** Application code should not depend on discipline
  ("please only read views") for data access control.
- **Decision:** Install a SQLite authorizer that allows base-table
  column reads only when SQLite reports an allowed view as the
  source, and denies direct reads, `sqlite_master`, writes, PRAGMA,
  and ATTACH. The empty-column view-expansion probe is allowed for
  known tables/views only, because it names no column.
- **Consequences:** Seeding must happen before guarding. Any new
  view needs an allowlist entry and a test.
