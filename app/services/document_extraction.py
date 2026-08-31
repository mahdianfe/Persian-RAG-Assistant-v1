from app.services.pdf_reconstruction import (
    PDFReconstructionService,
)
from app.services.pdf_structure import (
    ParsedDocument,
)
from app.services.text_normalizer import (
    PDFTextNormalizer,
)


class DocumentExtractionService:
    """
    Convert parsed PDF structure into plain text.
    """

    @classmethod
    def extract(
        cls,
        document: ParsedDocument,
    ) -> str:
        """
        Reconstruct and normalize document text.
        """

        pages: list[str] = []

        for page in document.pages:
            page_lines: list[str] = []

            for block in page.blocks:
                for line in block.lines:
                    reconstructed = (
                        PDFReconstructionService
                        .reconstruct_line(line)
                    )

                    normalized = (
                        PDFTextNormalizer
                        .normalize(reconstructed)
                    )

                    if normalized:
                        page_lines.append(
                            normalized
                        )

            if page_lines:
                pages.append(
                    "\n".join(page_lines)
                )

        return "\n\n".join(pages)
