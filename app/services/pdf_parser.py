from pathlib import Path

import pymupdf

from app.services.pdf_structure import (
    PDFBlock,
    PDFCharacter,
    PDFLine,
    PDFPage,
    ParsedDocument,
)


class PDFParser:
    """Parse PDF files into structured representations."""

    @classmethod
    def parse(
        cls,
        file_path: Path,
    ) -> ParsedDocument:
        """Parse PDF into document structure."""

        document = pymupdf.open(file_path)

        try:
            pages: list[PDFPage] = []

            for page_number, page in enumerate(
                document,
                start=1,
            ):
                parsed_page = cls._parse_page(
                    page_number,
                    page,
                )

                pages.append(parsed_page)

            return ParsedDocument(
                file_name=file_path.name,
                pages=pages,
            )

        finally:
            document.close()

    @classmethod
    def _parse_page(
        cls,
        page_number: int,
        page: pymupdf.Page,
    ) -> PDFPage:
        """Parse one PDF page."""

        raw = page.get_text(
            "rawdict",
        )

        blocks: list[PDFBlock] = []

        for block_number, block in enumerate(
            raw.get("blocks", []),
        ):
            if "lines" not in block:
                continue

            lines: list[PDFLine] = []

            for line in block["lines"]:
                characters = cls._extract_characters(
                    line,
                )

                if characters:
                    lines.append(
                        PDFLine(
                            characters=characters,
                        )
                    )

            if lines:
                blocks.append(
                    PDFBlock(
                        block_number=block_number,
                        bbox=tuple(
                            block["bbox"]
                        ),
                        lines=lines,
                    )
                )

        return PDFPage(
            page_number=page_number,
            width=page.rect.width,
            height=page.rect.height,
            blocks=blocks,
        )

    @staticmethod
    def _extract_characters(
        line: dict,
    ) -> list[PDFCharacter]:
        """Extract characters from one PDF line."""

        characters: list[PDFCharacter] = []

        for span in line.get(
            "spans",
            [],
        ):
            font_name = span.get(
                "font",
            )

            font_size = span.get(
                "size",
            )

            for char in span.get(
                "chars",
                [],
            ):
                bbox = char.get(
                    "bbox",
                )

                if not bbox:
                    continue

                characters.append(
                    PDFCharacter(
                        text=char.get(
                            "c",
                            "",
                        ),
                        x0=float(bbox[0]),
                        y0=float(bbox[1]),
                        x1=float(bbox[2]),
                        y1=float(bbox[3]),
                        font_name=font_name,
                        font_size=font_size,
                    )
                )

        return characters
