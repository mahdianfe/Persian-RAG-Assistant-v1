
import unicodedata


class PDFTextNormalizer:
    """Normalize extracted PDF text without changing text direction."""

    ZERO_WIDTH_CHARS = {
        "\u200b",
        "\u200c",
        "\u200d",
        "\u200e",
        "\u200f",
        "\ufeff",
    }

    @classmethod
    def normalize(cls, text: str) -> str:
        """
        Normalize unicode characters and invisible marks.

        BiDi processing is intentionally not applied here.
        """

        if not text:
            return ""

        text = unicodedata.normalize(
            "NFKC",
            text,
        )

        for char in cls.ZERO_WIDTH_CHARS:
            text = text.replace(
                char,
                "",
            )

        text = cls._normalize_spaces(text)

        return text.strip()

    @staticmethod
    def _normalize_spaces(text: str) -> str:
        """Normalize whitespace characters."""

        replacements = {
            "\u00a0": " ",
            "\t": " ",
            "\n": " ",
        }

        for old, new in replacements.items():
            text = text.replace(
                old,
                new,
            )

        while "  " in text:
            text = text.replace(
                "  ",
                " ",
            )

        return text
