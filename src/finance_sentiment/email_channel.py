"""Email channel: dry-run by default, explicit opt-in to send.

- Default ``dry_run=True``: ``send`` records nothing and sends nothing;
  it returns a dry-run result describing what *would* have been sent.
- Opting in requires constructing the channel with
  ``dry_run=False`` AND the environment must not be CI: in CI
  (``CI`` env var set to a truthy value) sending is refused outright.
- No credentials are read, stored, or sent by this module. The
  "send" path in this scaffold is a recorded simulation, not an SMTP
  connection, so a scaffold checkout can never email anyone by
  accident. A production adopter replaces ``_deliver`` with a real
  mailer behind its own approval flow.
"""

import os
from dataclasses import dataclass, field


class SendRefusedInCI(Exception):
    pass


@dataclass
class EmailResult:
    sent: bool
    dry_run: bool
    to: str
    subject: str
    body_preview: str


@dataclass
class EmailChannel:
    dry_run: bool = True
    sent_log: list = field(default_factory=list)

    def send(self, to, subject, body):
        if self.dry_run:
            return EmailResult(False, True, to, subject, body[:120])
        if os.environ.get("CI", "").lower() in ("1", "true", "yes"):
            raise SendRefusedInCI("email sending is refused in CI")
        result = self._deliver(to, subject, body)
        self.sent_log.append(result)
        return result

    def _deliver(self, to, subject, body):
        # Simulation only: no network, no credentials. See module docstring.
        return EmailResult(True, False, to, subject, body[:120])
