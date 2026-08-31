from pathlib import Path

from app.services.pdf import PDFService


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

PDF_PATH = (
    PROJECT_ROOT
    / "persian-rag-test-02.pdf"
)


def test_persian_pdf_extracts_expected_content() -> None:
    """Extract important Persian and English content from the PDF."""

    assert PDF_PATH.exists()

    text = PDFService.extract_text(
        PDF_PATH,
    )

    assert "جزوه مقدماتی یادگیری ماشین" in text
    assert "یادگیری ماشین" in text
    assert "scikit-learn" in text
    assert "Python" in text


def test_persian_pdf_preserves_mixed_direction_sentence() -> None:
    """Preserve logical order of a mixed Persian/English sentence."""

    text = PDFService.extract_text(
        PDF_PATH,
    )

    assert (
        "این سند برای آزمایش سیستم "
        "RAG فارسی ساخته شده است."
        in text
    )
