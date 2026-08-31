from app.services.text_normalizer import PDFTextNormalizer


def test_normalize_removes_zero_width_characters() -> None:
    text = "یاد\u200cگیری"

    result = PDFTextNormalizer.normalize(text)

    assert "\u200c" not in result


def test_normalize_keeps_persian_text() -> None:
    text = "یادگیری ماشین"

    result = PDFTextNormalizer.normalize(text)

    assert result == text


def test_normalize_unicode() -> None:
    text = "ﻣﺎﺷﯿﻦ"

    result = PDFTextNormalizer.normalize(text)

    assert result == "ماشین"



def test_normalize_arabic_presentation_forms() -> None:
    from app.services.text_normalizer import PDFTextNormalizer

    text = "ﺟﺰوه"

    result = PDFTextNormalizer.normalize(
        text,
    )

    assert result == "جزوه"


def test_normalize_mixed_persian_english_text() -> None:
    from app.services.text_normalizer import PDFTextNormalizer

    text = "ﺟﺰوه k-means"

    result = PDFTextNormalizer.normalize(
        text,
    )

    assert result == "جزوه k-means"
