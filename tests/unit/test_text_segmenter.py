from app.services.pdf_structure import PDFCharacter
from app.services.text_segmenter import TextSegmenter


def test_segment_mixed_rtl_ltr_text() -> None:
    characters = [
        PDFCharacter(
            text="م",
            x0=0,
            y0=0,
            x1=1,
            y1=1,
        ),
        PDFCharacter(
            text="د",
            x0=1,
            y0=0,
            x1=2,
            y1=1,
        ),
        PDFCharacter(
            text="k",
            x0=2,
            y0=0,
            x1=3,
            y1=1,
        ),
        PDFCharacter(
            text="-",
            x0=3,
            y0=0,
            x1=4,
            y1=1,
        ),
        PDFCharacter(
            text="m",
            x0=4,
            y0=0,
            x1=5,
            y1=1,
        ),
    ]

    result = TextSegmenter.segment(
        characters,
    )

    assert len(result) == 2

    assert result[0].direction == "RTL"
    assert result[1].direction == "LTR"
