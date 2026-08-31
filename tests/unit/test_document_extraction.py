from app.services.document_extraction import (
    DocumentExtractionService,
)
from app.services.pdf_structure import (
    PDFCharacter,
    PDFLine,
    PDFBlock,
    PDFPage,
    ParsedDocument,
)


def test_extract_reconstructs_document_text() -> None:
    document = ParsedDocument(
        file_name="test.pdf",
        pages=[
            PDFPage(
                page_number=1,
                width=595,
                height=842,
                blocks=[
                    PDFBlock(
                        block_number=0,
                        bbox=(
                            0,
                            0,
                            100,
                            100,
                        ),
                        lines=[
                            PDFLine(
                                characters=[
                                    PDFCharacter(
                                        text="k",
                                        x0=40,
                                        y0=0,
                                        x1=45,
                                        y1=10,
                                    ),
                                    PDFCharacter(
                                        text="-",
                                        x0=45,
                                        y0=0,
                                        x1=50,
                                        y1=10,
                                    ),
                                    PDFCharacter(
                                        text="m",
                                        x0=50,
                                        y0=0,
                                        x1=55,
                                        y1=10,
                                    ),
                                ],
                            )
                        ],
                    )
                ],
            )
        ],
    )

    result = DocumentExtractionService.extract(
        document,
    )

    assert result == "k-m"



def test_extract_normalizes_persian_presentation_forms() -> None:
    document = ParsedDocument(
        file_name="test.pdf",
        pages=[
            PDFPage(
                page_number=1,
                width=595,
                height=842,
                blocks=[
                    PDFBlock(
                        block_number=0,
                        bbox=(
                            0,
                            0,
                            100,
                            100,
                        ),
                        lines=[
                            PDFLine(
                                characters=[
                                    PDFCharacter(
                                        text="ﺟ",
                                        x0=40,
                                        y0=0,
                                        x1=45,
                                        y1=10,
                                    ),
                                    PDFCharacter(
                                        text="ﺰ",
                                        x0=35,
                                        y0=0,
                                        x1=40,
                                        y1=10,
                                    ),
                                    PDFCharacter(
                                        text="و",
                                        x0=30,
                                        y0=0,
                                        x1=35,
                                        y1=10,
                                    ),
                                    PDFCharacter(
                                        text="ه",
                                        x0=25,
                                        y0=0,
                                        x1=30,
                                        y1=10,
                                    ),
                                ],
                            )
                        ],
                    )
                ],
            )
        ],
    )

    result = DocumentExtractionService.extract(
        document,
    )

    assert result == "جزوه"
