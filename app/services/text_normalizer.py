import re
import unicodedata


class PDFTextNormalizer:
    """Normalize extracted PDF text without changing text direction."""

    ZERO_WIDTH_CHARS = {
        "\u200b",  # zero width space
        "\u200d",  # zero width joiner
        "\u200e",  # LRM
        "\u200f",  # RLM
        "\ufeff",  # BOM
    }

    @staticmethod
    def _remove_leading_punctuation(text: str) -> str:
        """
        Remove punctuation accidentally placed
        at the beginning of Persian sentences.
        """

        while text.startswith("."):
            text = text[1:]

        return text.lstrip()

    @staticmethod
    def _normalize_punctuation_spacing(text: str) -> str:
        """
        Normalize punctuation spacing.

        Example:
            Regression .برای

        becomes:
            Regression. برای
        """

        text = re.sub(
            r"\s+\.",
            ".",
            text,
        )


        text = re.sub(
            r"(?<!\d)\.(?=[\u0600-\u06FF])",
            ". ",
            text,
        )

        return text


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

        text = re.sub(
            r"([A-Za-z])\.\s+(?=[\u0600-\u06FF])",
            r"\1 ",
            text,
        )

        text = cls._remove_leading_punctuation(
            text,
        )

        text = cls._normalize_punctuation_spacing(text)

        return text.strip()

    @staticmethod
    def _normalize_spaces(text: str) -> str:
        """Normalize whitespace characters."""

        replacements = {
            "\u00a0": " ",
            "\t": " ",
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

        while "\n\n\n" in text:
            text = text.replace(
                "\n\n\n",
                "\n\n",
            )

        return text
