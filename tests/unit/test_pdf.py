from pathlib import Path
from unittest.mock import Mock, patch

from app.services.pdf import PDFService


def make_page(text: str) -> Mock:
    page = Mock()

    characters = []

    if text and all(
        "\u0600" <= char <= "\u06ff" or char.isspace()
        for char in text
    ):
        # Persian / Arabic:
        # PDF reconstruction expects RTL characters
        # in visual order from right to left.
        for index, char in enumerate(text):
            x1 = 100 - (index * 10)
            x0 = x1 - 10

            characters.append(
                {
                    "c": char,
                    "bbox": (
                        x0,
                        0,
                        x1,
                        10,
                    ),
                }
            )
    else:
        # LTR text.
        for index, char in enumerate(text):
            x0 = index * 10
            x1 = x0 + 10

            characters.append(
                {
                    "c": char,
                    "bbox": (
                        x0,
                        0,
                        x1,
                        10,
                    ),
                }
            )

    page.get_text.return_value = {
        "blocks": [
            {
                "bbox": (
                    0,
                    0,
                    100,
                    20,
                ),
                "lines": [
                    {
                        "spans": [
                            {
                                "font": "TestFont",
                                "size": 12,
                                "chars": characters,
                            }
                        ]
                    }
                ],
            }
        ]
    }

    return page


def make_empty_page() -> Mock:
    page = Mock()

    page.get_text.return_value = {
        "blocks": [],
    }

    return page


def make_document(
    pages: list[Mock],
) -> Mock:
    document = Mock()

    document.__iter__ = Mock(
        return_value=iter(pages),
    )

    document.close = Mock()

    return document


def test_extract_text_preserves_page_boundaries() -> None:
    first_page = make_page(
        "متن صفحه اول",
    )

    second_page = make_page(
        "متن صفحه دوم",
    )

    document = make_document(
        [
            first_page,
            second_page,
        ]
    )

    with patch(
        "app.services.pdf.pymupdf.open",
        return_value=document,
    ):
        result = PDFService.extract_text(
            Path("test.pdf"),
        )

    assert "--- PAGE 1 ---" in result
    assert "--- PAGE 2 ---" in result

    assert "متن" in result
    assert "صفحه" in result
    assert "اول" in result
    assert "دوم" in result


def test_extract_text_ignores_empty_pages() -> None:
    empty_page = make_empty_page()

    page = make_page(
        "متن",
    )

    document = make_document(
        [
            empty_page,
            page,
        ]
    )

    with patch(
        "app.services.pdf.pymupdf.open",
        return_value=document,
    ):
        result = PDFService.extract_text(
            Path("test.pdf"),
        )

    assert "--- PAGE 1 ---" not in result
    assert "--- PAGE 2 ---" in result
    assert "متن" in result
