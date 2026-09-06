from app.services.extractor import ExtractionService


def test_extract_algorithm_terms():
    question = "چه الگوریتم‌هایی در متن نام برده شده‌اند؟"

    context = """
    الگوریتم‌های Regression و Classification
    و k-means و Clustering در متن معرفی شده‌اند.
    """

    result = ExtractionService.extract_terms(
        question,
        context,
    )

    assert result is not None

    assert "Regression" in result
    assert "Classification" in result
    assert "k-means" in result
    assert "Clustering" in result


def test_extract_word_terms():
    question = "چه واژه‌هایی مانند Python و RAG در متن آمده‌اند؟"

    context = """
    ابزارهای Python، RAG، PDF و scikit-learn
    در متن استفاده شده‌اند.
    """

    result = ExtractionService.extract_terms(
        question,
        context,
    )

    assert result is not None

    assert "Python" in result
    assert "RAG" in result
    assert "PDF" in result
    assert "scikit-learn" in result


def test_extract_returns_none_when_not_supported():
    question = "آب و هوا چگونه است؟"

    context = """
    این متن درباره یادگیری ماشین است.
    """

    result = ExtractionService.extract_terms(
        question,
        context,
    )

    assert result is None
