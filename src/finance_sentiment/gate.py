"""Reliability gate + human-confirmation gate.

Two gates, deliberately separate:

1. ReliabilityGate answers whether a score may be acted on. It
   blocks (routes to HUMAN_REVIEW) when the absolute score is below
   the calibrated threshold, when too few sentiment hits support it,
   or when the text is too short. ``act()`` on a blocked decision
   without a confirmed human approval raises GateBlocked: there is
   no bypass path around the gate.

2. ConfirmationGate issues named-person, single-use, scoped,
   expiring approvals and checks consent strictly:
   - no approval at all            -> ApprovalAbsent (bypass attempt)
   - unknown approval id            -> ApprovalAbsent (absent path)
   - consent "no" / "reject"        -> Rejected (reject path)
   - consent "yes" at low confidence (< 0.5) -> LowConfidenceRejected
   - consent containing both yes and no, e.g. "yes, wait, no"
     -> ContradictingConsentRejected
   - expired or already-used approval -> ApprovalExpired / AlreadyUsed
   An approval is consumed on any terminal decision (approve or
   reject), so it cannot be replayed.
"""

import re
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from .scorer import SentimentResult

_YES = re.compile(r"\b(yes|approve|approved|confirm|confirmed)\b")
_NO = re.compile(r"\b(no|reject|rejected|decline|declined)\b")


class GateBlocked(Exception):
    pass


class ApprovalAbsent(Exception):
    pass


class ApprovalExpired(Exception):
    pass


class ApprovalAlreadyUsed(Exception):
    pass


class Rejected(Exception):
    pass


class LowConfidenceRejected(Exception):
    pass


class ContradictingConsentRejected(Exception):
    pass


@dataclass
class ReliabilityDecision:
    action: str  # "ACT" or "HUMAN_REVIEW"
    reason: str
    score: float
    label: str


class ReliabilityGate:
    def __init__(self, threshold=0.30, min_hits=2, min_words=8):
        if threshold < 0:
            raise ValueError("threshold must not be negative")
        self.threshold = threshold
        self.min_hits = min_hits
        self.min_words = min_words

    def decide(self, result):
        if abs(result.score) < self.threshold:
            return ReliabilityDecision("HUMAN_REVIEW", "score below threshold",
                                       result.score, result.label)
        if result.hits < self.min_hits:
            return ReliabilityDecision("HUMAN_REVIEW", "too few sentiment hits",
                                       result.score, result.label)
        if result.word_count < self.min_words:
            return ReliabilityDecision("HUMAN_REVIEW", "text too short",
                                       result.score, result.label)
        return ReliabilityDecision("ACT", "score meets reliability bar",
                                   result.score, result.label)

    def act(self, decision, confirmed_approval=None):
        """Act on a decision. A blocked decision needs a confirmed approval.

        ``confirmed_approval`` must be the string "CONFIRMED" returned
        by ConfirmationGate.confirm; anything else is a bypass attempt.
        """
        if decision.action == "ACT":
            return {"acted": True, "human_override": False}
        if confirmed_approval != "CONFIRMED":
            raise GateBlocked(
                "decision is HUMAN_REVIEW: a confirmed human approval is required"
            )
        return {"acted": True, "human_override": True}


@dataclass
class Approval:
    approval_id: str
    approver: str
    scope: str
    expires_at: datetime
    used: bool = False


class ConfirmationGate:
    def __init__(self, ttl_seconds=3600):
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self.ttl_seconds = ttl_seconds
        self._approvals = {}

    def request(self, approver, scope):
        """Create an approval. Approver must be a named person."""
        if not approver or not approver.strip():
            raise ValueError("approver must be a named person, not blank")
        if not scope or not scope.strip():
            raise ValueError("scope must not be blank")
        approval = Approval(
            approval_id=secrets.token_hex(8),
            approver=approver.strip(),
            scope=scope.strip(),
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=self.ttl_seconds),
        )
        self._approvals[approval.approval_id] = approval
        return approval

    def confirm(self, approval_id, approver, consent_text, confidence=1.0,
                scope=None):
        """Confirm (or reject) an approval. Returns "CONFIRMED" on approval."""
        if approval_id is None:
            raise ApprovalAbsent("no approval supplied (bypass attempt)")
        approval = self._approvals.get(approval_id)
        if approval is None:
            raise ApprovalAbsent(f"unknown approval id: {approval_id}")
        if approval.used:
            raise ApprovalAlreadyUsed("approval has already been used")
        if datetime.now(timezone.utc) > approval.expires_at:
            raise ApprovalExpired("approval has expired")
        if approver != approval.approver:
            raise ApprovalAbsent("approver does not match the named approver")
        if scope is not None and scope != approval.scope:
            raise ApprovalAbsent("scope does not match the approval scope")
        text = (consent_text or "").lower()
        has_yes = bool(_YES.search(text))
        has_no = bool(_NO.search(text))
        approval.used = True
        if has_yes and has_no:
            raise ContradictingConsentRejected(
                "consent contains both yes and no (e.g. 'yes, wait, no')"
            )
        if has_no or not has_yes:
            raise Rejected("consent was not an approval")
        if confidence < 0.5:
            raise LowConfidenceRejected("approval confidence below 0.5")
        return "CONFIRMED"
