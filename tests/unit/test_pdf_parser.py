from pathlib import Path

from app.services.pdf_parser import PDFParser


def test_parse_pdf_returns_document_structure(
    tmp_path: Path,
) -> None:
    pdf_path = tmp_path / "sample.pdf"

    import pymupdf

    doc = pymupdf.open()

    page = doc.new_page()

    page.insert_text(
        (50, 50),
        "سلام دنیا",
    )

    doc.save(pdf_path)

    doc.close()

    result = PDFParser.parse(
        pdf_path,
    )

    assert result.file_name == "sample.pdf"

    assert len(result.pages) == 1

    page = result.pages[0]

    assert page.page_number == 1

    assert len(page.blocks) > 0

    assert len(page.blocks[0].lines) > 0

    assert (
        page.blocks[0]
        .lines[0]
        .text
        .strip()
        != ""
    )
