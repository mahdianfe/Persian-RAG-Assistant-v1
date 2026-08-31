import re


class TextChunkingService:
    """Split text into semantic or overlapping chunks."""

    SECTION_PATTERN = re.compile(
        r"^\s*[۰-۹0-9]+\s*[.٫]\s*[۰-۹0-9]+\s+(.+?)\s*$"
    )

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than zero."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> list[str]:
        """
        Split text while preserving paragraph boundaries when possible.

        Plain text without paragraph breaks uses overlapping character
        windows. Text containing paragraphs is chunked paragraph-aware.
        """

        text = text.strip()

        if not text:
            return []

        if "\n\n" not in text:
            return self._split_text(text)

        paragraphs = [
            paragraph.strip()
            for paragraph in re.split(r"\n\s*\n", text)
            if paragraph.strip()
        ]

        chunks: list[str] = []
        current: list[str] = []
        current_length = 0

        for paragraph in paragraphs:
            paragraph_length = len(paragraph)

            # Very large paragraph: flush current content first,
            # then split the paragraph separately.
            if paragraph_length > self.chunk_size:
                if current:
                    chunks.append("\n\n".join(current))
                    current = []
                    current_length = 0

                chunks.extend(
                    self._split_text(paragraph)
                )
                continue

            additional_length = paragraph_length

            if current:
                additional_length += 2

            if (
                current
                and current_length + additional_length
                > self.chunk_size
            ):
                chunks.append("\n\n".join(current))

                # Preserve paragraph overlap only when the previous
                # paragraph itself fits safely.
                overlap_paragraphs: list[str] = []
                overlap_length = 0

                for previous in reversed(current):
                    previous_length = len(previous)

                    if (
                        overlap_length
                        + previous_length
                        + (2 if overlap_paragraphs else 0)
                        > self.chunk_overlap
                    ):
                        break

                    overlap_paragraphs.insert(
                        0,
                        previous,
                    )

                    overlap_length += (
                        previous_length
                        + (2 if overlap_paragraphs else 0)
                    )

                current = overlap_paragraphs

                current_length = len(
                    "\n\n".join(current)
                )

            current.append(paragraph)

            current_length = len(
                "\n\n".join(current)
            )

        if current:
            chunks.append("\n\n".join(current))

        return chunks

    def split_sections(self, text: str) -> list[str]:
        """
        Split a document by semantic section headings.

        Large sections are further split into paragraph-aware chunks.
        """

        text = text.strip()

        if not text:
            return []

        lines = text.splitlines()

        sections: list[str] = []
        current_section: list[str] = []

        for line in lines:
            stripped = line.strip()

            if not stripped:
                if current_section and current_section[-1] != "":
                    current_section.append("")
                continue

            if self.SECTION_PATTERN.match(stripped):
                if current_section:
                    section = "\n".join(
                        current_section
                    ).strip()

                    if section:
                        sections.append(section)

                current_section = [stripped]
                continue

            current_section.append(stripped)

        if current_section:
            section = "\n".join(
                current_section
            ).strip()

            if section:
                sections.append(section)

        final_chunks: list[str] = []

        for section in sections:
            if len(section) <= self.chunk_size:
                final_chunks.append(section)
            else:
                final_chunks.extend(
                    self.split(section)
                )

        return final_chunks

    def _split_text(self, text: str) -> list[str]:
        """Split plain text using overlapping character windows."""

        if not text:
            return []

        chunks: list[str] = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(text):
                break

            next_start = end - self.chunk_overlap

            # Never start an overlapping chunk in the middle
            # of a word when a whitespace boundary is available.
            if (
                next_start > 0
                and next_start < len(text)
                and not text[next_start].isspace()
            ):
                whitespace_position = text.find(
                    " ",
                    next_start,
                    min(
                        len(text),
                        next_start + 50,
                    ),
                )

                if whitespace_position != -1:
                    next_start = whitespace_position + 1

            start = next_start

        return chunks
