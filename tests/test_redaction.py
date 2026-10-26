from finance_sentiment.redaction import redact


def test_redaction_removes_card_number():
    result = redact("Charge to card 4111 1111 1111 1111 for the order.")
    assert "4111" not in result.text
    assert "[CARD REDACTED]" in result.text
    assert "card_number" in result.found


def test_redaction_removes_dashed_card_number():
    result = redact("Card 4111-1111-1111-1111 on file.")
    assert "4111" not in result.text
    assert "card_number" in result.found


def test_redaction_removes_email_address():
    result = redact("Contact analyst@example.com for details.")
    assert "analyst@example.com" not in result.text
    assert "[EMAIL REDACTED]" in result.text
    assert "email" in result.found


def test_redaction_removes_ssn():
    result = redact("SSN 123-45-6789 was in the note.")
    assert "123-45-6789" not in result.text
    assert "ssn" in result.found


def test_redaction_removes_phone_number():
    result = redact("Call +1 555 123 4567 for details.")
    assert "555 123 4567" not in result.text
    assert "phone" in result.found


def test_redaction_leaves_clean_text_unchanged():
    text = "Revenue grew strongly and demand remained robust."
    result = redact(text)
    assert result.text == text and result.found == []


def test_redaction_reports_all_types_found():
    result = redact("Card 4111 1111 1111 1111, email a@b.com, phone +1 555 123 4567.")
    assert set(result.found) >= {"card_number", "email", "phone"}
