import pytest

from finance_sentiment.gate import (
    ApprovalAbsent, ApprovalAlreadyUsed, ApprovalExpired, ConfirmationGate,
    ContradictingConsentRejected, GateBlocked, LowConfidenceRejected,
    Rejected, ReliabilityGate,
)
from finance_sentiment.scorer import score_text


def _strong_positive():
    return score_text(
        "Revenue grew strongly, margins expanded, and demand remained "
        "robust across regions.")


def _weak_text():
    return score_text("Revenue grew a little.")


# --- Reliability gate ---

def test_reliability_gate_acts_on_strong_score():
    decision = ReliabilityGate().decide(_strong_positive())
    assert decision.action == "ACT"


def test_reliability_gate_blocks_weak_score_to_human_review():
    decision = ReliabilityGate().decide(_weak_text())
    assert decision.action == "HUMAN_REVIEW"


def test_reliability_gate_blocks_short_text():
    decision = ReliabilityGate().decide(score_text("growth strong"))
    assert decision.action == "HUMAN_REVIEW"


def test_reliability_gate_act_bypass_raises_gate_blocked():
    decision = ReliabilityGate().decide(_weak_text())
    with pytest.raises(GateBlocked):
        ReliabilityGate().act(decision)


def test_reliability_gate_act_with_confirmed_approval_allows_override():
    decision = ReliabilityGate().decide(_weak_text())
    result = ReliabilityGate().act(decision, confirmed_approval="CONFIRMED")
    assert result["acted"] is True and result["human_override"] is True


def test_reliability_gate_rejects_negative_threshold():
    with pytest.raises(ValueError):
        ReliabilityGate(threshold=-0.1)


# --- Confirmation gate: bypass / reject / absent / low-confidence / contradicting ---

def test_confirmation_gate_bypass_without_approval_raises_absent():
    gate = ConfirmationGate()
    with pytest.raises(ApprovalAbsent):
        gate.confirm(None, "Ada Analyst", "yes")


def test_confirmation_gate_absent_unknown_id_raises_absent():
    gate = ConfirmationGate()
    with pytest.raises(ApprovalAbsent):
        gate.confirm("does-not-exist", "Ada Analyst", "yes")


def test_confirmation_gate_reject_consent_no_raises_rejected():
    gate = ConfirmationGate()
    approval = gate.request("Ada Analyst", "act-on-call-01")
    with pytest.raises(Rejected):
        gate.confirm(approval.approval_id, "Ada Analyst", "no")


def test_confirmation_gate_reject_wrong_approver_raises_absent():
    gate = ConfirmationGate()
    approval = gate.request("Ada Analyst", "act-on-call-01")
    with pytest.raises(ApprovalAbsent):
        gate.confirm(approval.approval_id, "Someone Else", "yes")


def test_confirmation_gate_low_confidence_yes_raises():
    gate = ConfirmationGate()
    approval = gate.request("Ada Analyst", "act-on-call-01")
    with pytest.raises(LowConfidenceRejected):
        gate.confirm(approval.approval_id, "Ada Analyst", "yes", confidence=0.3)


def test_confirmation_gate_self_contradicting_consent_raises():
    gate = ConfirmationGate()
    approval = gate.request("Ada Analyst", "act-on-call-01")
    with pytest.raises(ContradictingConsentRejected):
        gate.confirm(approval.approval_id, "Ada Analyst", "yes, wait, no")


def test_confirmation_gate_happy_path_confirms_once():
    gate = ConfirmationGate()
    approval = gate.request("Ada Analyst", "act-on-call-01")
    assert gate.confirm(approval.approval_id, "Ada Analyst", "yes") == "CONFIRMED"
    with pytest.raises(ApprovalAlreadyUsed):
        gate.confirm(approval.approval_id, "Ada Analyst", "yes")


def test_confirmation_gate_expired_approval_raises():
    gate = ConfirmationGate(ttl_seconds=3600)
    approval = gate.request("Ada Analyst", "act-on-call-01")
    approval.expires_at = approval.expires_at.replace(year=2000)
    with pytest.raises(ApprovalExpired):
        gate.confirm(approval.approval_id, "Ada Analyst", "yes")


def test_confirmation_gate_requires_named_person_and_scope():
    gate = ConfirmationGate()
    with pytest.raises(ValueError):
        gate.request("", "act-on-call-01")
    with pytest.raises(ValueError):
        gate.request("Ada Analyst", "")


def test_confirmation_gate_scope_mismatch_raises_absent():
    gate = ConfirmationGate()
    approval = gate.request("Ada Analyst", "act-on-call-01")
    with pytest.raises(ApprovalAbsent):
        gate.confirm(approval.approval_id, "Ada Analyst", "yes",
                     scope="act-on-something-else")
