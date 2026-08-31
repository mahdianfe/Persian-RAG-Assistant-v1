from dataclasses import dataclass, field


@dataclass
class PDFCharacter:
    """Single character extracted from PDF with geometry."""

    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    font_name: str | None = None
    font_size: float | None = None


@dataclass
class PDFLine:
    """A line of text inside a PDF block."""

    characters: list[PDFCharacter] = field(
        default_factory=list,
    )

    @property
    def text(self) -> str:
        """Return raw line text."""

        return "".join(
            character.text
            for character in self.characters
        )


@dataclass
class PDFBlock:
    """A logical PDF block."""

    block_number: int
    bbox: tuple[
        float,
        float,
        float,
        float,
    ]

    lines: list[PDFLine] = field(
        default_factory=list,
    )


@dataclass
class PDFPage:
    """Single PDF page representation."""

    page_number: int
    width: float
    height: float

    blocks: list[PDFBlock] = field(
        default_factory=list,
    )


@dataclass
class ParsedDocument:
    """Complete parsed PDF document."""

    file_name: str
    pages: list[PDFPage] = field(
        default_factory=list,
    )
