from pathlib import Path

import pymupdf

from app.services.pdf_parser import PDFParser
from app.services.pdf_reconstruction import PDFReconstructionService
from app.services.text_normalizer import PDFTextNormalizer


class PDFService:
    """Service for extracting text from PDF files."""

    @classmethod
    def extract_text(
        cls,
        file_path: Path,
    ) -> str:
        """Extract and reconstruct text from a PDF."""

        document = PDFParser.parse(
            file_path,
        )

        pages: list[str] = []

        for page in document.pages:
            page_lines: list[str] = []

            for block in page.blocks:
                for line in block.lines:
                    text = PDFReconstructionService.reconstruct_line(
                        line,
                    )

                    if text:
                        page_lines.append(text)

            page_text = "\n".join(
                page_lines,
            )

            if page_text.strip():
                pages.append(
                    f"--- PAGE {page.page_number} ---\n"
                    f"{page_text.strip()}"
                )

        return PDFTextNormalizer.normalize(
            "\n\n".join(pages),
        )
