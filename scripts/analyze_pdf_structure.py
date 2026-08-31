from pathlib import Path

from app.services.pdf_parser import PDFParser


PDF_PATH = Path(
    "/home/fatemeh/downloads/persian-rag-real.pdf"
)


def main() -> None:
    document = PDFParser.parse(
        PDF_PATH,
    )

    print(
        f"File: {document.file_name}"
    )

    print(
        f"Pages: {len(document.pages)}"
    )

    for page in document.pages:
        print("\n" + "=" * 60)

        print(
            f"PAGE {page.page_number}"
        )

        print(
            f"Size: {page.width} x {page.height}"
        )

        print(
            f"Blocks: {len(page.blocks)}"
        )

        for block in page.blocks:
            print(
                "\nBLOCK",
                block.block_number,
                "bbox=",
                block.bbox,
            )

            print(
                "Lines:",
                len(block.lines),
            )

            for line in block.lines[:3]:
                print(
                    "   ",
                    repr(
                        line.text[:100]
                    )
                )


if __name__ == "__main__":
    main()
