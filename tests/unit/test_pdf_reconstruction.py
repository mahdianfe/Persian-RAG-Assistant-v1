from app.services.pdf_reconstruction import (
    PDFReconstructionService,
)
from app.services.pdf_structure import (
    PDFCharacter,
    PDFLine,
)


def make_character(
    text: str,
    x0: float,
    x1: float,
) -> PDFCharacter:
    return PDFCharacter(
        text=text,
        x0=x0,
        y0=0,
        x1=x1,
        y1=10,
    )


def test_reconstruct_line_preserves_rtl_character_order() -> None:
    line = PDFLine(
        characters=[
            make_character("س", 30, 35),
            make_character("ل", 20, 25),
            make_character("ا", 10, 15),
        ]
    )

    result = PDFReconstructionService.reconstruct_line(
        line,
    )

    assert result == "سلا"


def test_reconstruct_line_keeps_ltr_token() -> None:
    line = PDFLine(
        characters=[
            make_character("k", 40, 45),
            make_character("-", 45, 50),
            make_character("m", 50, 55),
        ]
    )

    result = PDFReconstructionService.reconstruct_line(
        line,
    )

    assert result == "k-m"


def test_reconstruct_line_keeps_scikit_learn() -> None:
    text = "scikit-learn"

    line = PDFLine(
        characters=[
            make_character(
                char,
                10 + index,
                11 + index,
            )
            for index, char in enumerate(text)
        ]
    )

    result = PDFReconstructionService.reconstruct_line(
        line,
    )

    assert result == "scikit-learn"


def test_reconstruct_line_preserves_presentation_forms() -> None:
    line = PDFLine(
        characters=[
            make_character("ﺟ", 40, 45),
            make_character("ﺰ", 35, 40),
            make_character("و", 30, 35),
            make_character("ه", 25, 30),
        ]
    )

    result = PDFReconstructionService.reconstruct_line(
        line,
    )

    assert result == "جزوه"


def test_reconstruct_line_inserts_rtl_word_space_from_geometry() -> None:
    line = PDFLine(
        characters=[
            make_character("م", 60, 65),
            make_character("د", 55, 60),
            make_character("ل", 50, 55),
            make_character("خ", 40, 45),
            make_character("و", 35, 40),
            make_character("ب", 30, 35),
        ]
    )

    result = PDFReconstructionService.reconstruct_line(
        line,
    )

    assert result == "مدل خوب"


def test_reconstruct_line_inserts_ltr_word_space_from_geometry() -> None:
    line = PDFLine(
        characters=[
            make_character("a", 10, 15),
            make_character("b", 15, 20),
            make_character("c", 25, 30),
            make_character("d", 30, 35),
        ]
    )

    result = PDFReconstructionService.reconstruct_line(
        line,
    )

    assert result == "ab cd"


def test_reconstruct_line_does_not_duplicate_explicit_space() -> None:
    line = PDFLine(
        characters=[
            make_character("a", 10, 15),
            make_character(" ", 15, 20),
            make_character("b", 20, 25),
        ]
    )

    result = PDFReconstructionService.reconstruct_line(
        line,
    )

    assert result == "a b"


def test_reconstruct_line_keeps_embedded_english_word() -> None:
    line = PDFLine(
        characters=[
            make_character("م", 70, 75),
            make_character("د", 65, 70),
            make_character("ل", 60, 65),

            make_character("s", 55, 60),
            make_character("c", 50, 55),
            make_character("i", 45, 50),
            make_character("k", 40, 45),
            make_character("i", 35, 40),
            make_character("t", 30, 35),
            make_character("-", 25, 30),
            make_character("l", 20, 25),
            make_character("e", 15, 20),
            make_character("a", 10, 15),
            make_character("r", 5, 10),
            make_character("n", 0, 5),
        ]
    )

    result = PDFReconstructionService.reconstruct_line(
        line,
    )

    assert result == "مدل scikit-learn"
