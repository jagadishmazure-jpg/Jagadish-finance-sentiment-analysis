# Guardrails and security controls

| Control | How it is enforced | Proof test |
|---|---|---|
| View-only SQLite reads | Authorizer: base-table reads allowed only via an allowed view (source argument) or the empty-column view-expansion probe; `sqlite_master`, writes, PRAGMA, ATTACH, `load_extension` denied | `test_authorizer_denies_direct_base_table_read`, `test_authorizer_denies_sqlite_master_read`, `test_authorizer_denies_pragma`, `test_authorizer_denies_attach`, `test_authorizer_denies_write_insert` |
| Reliability gate | Threshold 0.30, min 2 hits, min 8 words; blocked decisions need a confirmed approval, no bypass | `test_reliability_gate_act_bypass_raises_gate_blocked`, `test_reliability_gate_blocks_weak_score_to_human_review` |
| Confirmation gate | Named-person, single-use, scoped, expiring approvals | `test_confirmation_gate_happy_path_confirms_once`, `test_confirmation_gate_expired_approval_raises`, `test_confirmation_gate_scope_mismatch_raises_absent` |
| Consent strictness | Reject on "no", absent on unknown/missing approval, low-confidence rejection, contradicting-consent rejection | `test_confirmation_gate_reject_consent_no_raises_rejected`, `test_confirmation_gate_bypass_without_approval_raises_absent`, `test_confirmation_gate_low_confidence_yes_raises`, `test_confirmation_gate_self_contradicting_consent_raises` |
| PII redaction | Card numbers, emails, phones, SSNs replaced with typed placeholders | `test_redaction_removes_card_number`, `test_redaction_removes_email_address`, `test_redaction_removes_phone_number`, `test_redaction_removes_ssn` |
| Row cap | `fetchmany(MAX + 1)` at fetch time; no `fetchall`, no LIMIT rewriting | `test_row_cap_raises_when_result_exceeds_cap` |
| Cost inputs | Negative amounts raise, never clamp | `test_negative_cost_rejected_not_clamped`, `test_budget_rejects_negative_add_and_limit` |
| Brand check | Hashed blocklist, asserted non-empty in a test | `test_brand_blocklist_is_non_empty` |
| Email | Dry-run by default, explicit opt-in, refused in CI, no credentials | `test_email_channel_dry_run_by_default_sends_nothing`, `test_email_channel_refused_in_ci_even_when_opted_in` |

Rule applied throughout: if a doc claims something is enforced,
a named test above proves it. If a test is missing, the claim is
removed, not softened.
