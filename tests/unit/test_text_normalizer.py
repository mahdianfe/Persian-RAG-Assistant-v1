from app.services.text_normalizer import PDFTextNormalizer


def test_normalize_preserves_persian_zwnj() -> None:
    text = "یاد\u200cگیری"

    result = PDFTextNormalizer.normalize(text)

    assert "\u200c" in result


def test_normalize_keeps_persian_text() -> None:
    text = "یادگیری ماشین"

    result = PDFTextNormalizer.normalize(text)

    assert result == text


def test_normalize_unicode() -> None:
    text = "ﻣﺎﺷﯿﻦ"

    result = PDFTextNormalizer.normalize(text)

    assert result == "ماشین"


def test_normalize_arabic_presentation_forms() -> None:
    text = "ﺟﺰوه"

    result = PDFTextNormalizer.normalize(
        text,
    )

    assert result == "جزوه"


def test_normalize_mixed_persian_english_text() -> None:
    text = "ﺟﺰوه k-means"

    result = PDFTextNormalizer.normalize(
        text,
    )

    assert result == "جزوه k-means"


def test_normalize_removes_other_zero_width_characters() -> None:
    text = "سلام\u200bدنیا"

    result = PDFTextNormalizer.normalize(text)

    assert "\u200b" not in result


def test_normalize_fixes_leading_punctuation() -> None:
    text = ".برای تست"

    result = PDFTextNormalizer.normalize(text)

    assert result.startswith("برای")


def test_normalize_moves_leading_punctuation_after_word() -> None:
    text = "Regression .برای تست"

    result = PDFTextNormalizer.normalize(text)

    assert result == "Regression. برای تست"


def test_normalize_preserves_decimal_numbers() -> None:
    text = "مقدار 3.14 است."

    result = PDFTextNormalizer.normalize(text)

    assert result == "مقدار 3.14 است."

def test_normalize_does_not_move_english_sentence_period() -> None:
    text = "Regression. برای تست استفاده می‌شود"

    result = PDFTextNormalizer.normalize(text)

    assert result == "Regression برای تست استفاده می‌شود"
