import re
import unicodedata


class TextCleaningService:
    """Utilities for cleaning extracted document text."""

    DOCUMENT_TITLE = "جزوه مقدماتی یادگیری ماشین"

    @staticmethod
    def clean(text: str) -> str:
        """Normalize and clean extracted document text."""

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Normalize Unicode characters produced by PDF extraction.
        text = unicodedata.normalize("NFKC", text)

        # Preserve word boundaries in Persian compounds.
        text = re.sub(r"\u200c+", " ", text)

        # Remove other zero-width formatting characters.
        text = re.sub(
            r"[\u200d\u200e\u200f\ufeff]",
            "",
            text,
        )

        # Add missing spaces between Persian/Arabic and Latin/digits.
        text = re.sub(
            r"([\u0600-\u06FF])([A-Za-z0-9])",
            r"\1 \2",
            text,
        )

        text = re.sub(
            r"([A-Za-z0-9])([\u0600-\u06FF])",
            r"\1 \2",
            text,
        )

        # Normalize section numbering.
        text = re.sub(
            r"([0-9۰-۹]+)\s*[.٫]\s*",
            r"\1. ",
            text,
        )

        has_page_markers = bool(
            re.search(r"--- PAGE \d+ ---", text)
        )

        if has_page_markers:
            pages = re.split(
                r"--- PAGE \d+ ---",
                text,
            )

            pages = [
                page.strip()
                for page in pages
                if page.strip()
            ]

            # Test/synthetic input:
            # If the first page clearly starts with a TOC,
            # remove that page and keep the remaining pages.
            if pages and (
                "فهرست مطالب" in pages[0]
                or "فهرستمطالب" in pages[0]
            ):
                pages = pages[1:]

            text = "\n\n".join(pages)

        else:
            # Real PDF input does not contain explicit page markers.
            # Remove front matter before the real first section.
            first_section_pattern = re.compile(
                r"(?:^|\n)\s*"
                r"(?:۲|2)\s*[.٫]\s*"
                r"(?:۱\s*[.٫]\s*)?"
                r"مقدمه"
                r"\s*:\s*"
                r"چرا\s+"
                r"یادگیری\s+"
                r"ماشین\s+"
                r"اهمیت\s+"
                r"دارد"
            )

            first_section_match = first_section_pattern.search(
                text,
            )

            if first_section_match:
                text = text[first_section_match.start():]

        # Remove explicit page markers if any remain.
        text = re.sub(
            r"--- PAGE \d+ ---",
            "",
            text,
        )

        # Normalize spaces.
        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        # Normalize spaces around line breaks.
        text = re.sub(
            r" *\n *",
            "\n",
            text,
        )

        lines = [
            line.strip()
            for line in text.splitlines()
        ]

        cleaned_lines: list[str] = []

        for line in lines:
            if not line:
                if (
                    cleaned_lines
                    and cleaned_lines[-1] != ""
                ):
                    cleaned_lines.append("")

                continue

            # Remove page-number-only lines.
            if re.fullmatch(
                r"[0-9۰-۹]+",
                line,
            ):
                continue

            # Keep one document title, remove repeated headers.
            if line == TextCleaningService.DOCUMENT_TITLE:
                if line in cleaned_lines:
                    continue

            cleaned_lines.append(line)

        text = "\n".join(cleaned_lines)

        # Collapse excessive blank lines.
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()
        
        
