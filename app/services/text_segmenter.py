from app.services.pdf_structure import PDFCharacter
from app.services.text_direction import (
    is_ltr_character,
    is_number_character,
    is_rtl_character,
)
from app.services.text_segment import TextSegment


class TextSegmenter:
    """Split characters into directional text segments."""

    @classmethod
    def segment(
        cls,
        characters: list[PDFCharacter],
    ) -> list[TextSegment]:
        """Group characters by logical direction."""

        if not characters:
            return []

        directions = [
            cls._get_direction(
                character.text,
            )
            for character in characters
        ]

        directions = cls._merge_neutral(
            directions,
        )

        segments: list[TextSegment] = []

        current_chars: list[str] = []
        current_direction = directions[0]

        for character, direction in zip(
            characters,
            directions,
        ):
            if direction != current_direction:
                segments.append(
                    TextSegment(
                        text="".join(
                            current_chars
                        ),
                        direction=current_direction,
                    )
                )

                current_chars = []
                current_direction = direction

            current_chars.append(
                character.text,
            )

        if current_chars:
            segments.append(
                TextSegment(
                    text="".join(current_chars),
                    direction=current_direction,
                )
            )

        return segments

    @classmethod
    def _merge_neutral(
        cls,
        directions: list[str],
    ) -> list[str]:
        """
        Attach neutral characters to surrounding direction.
        """

        result = directions.copy()

        for index, direction in enumerate(
            directions,
        ):
            if direction != "NEUTRAL":
                continue

            previous = None
            next_direction = None

            if index > 0:
                previous = directions[index - 1]

            if index < len(directions) - 1:
                next_direction = directions[index + 1]

            if (
                previous == "LTR"
                or next_direction == "LTR"
            ):
                result[index] = "LTR"

            elif (
                previous == "RTL"
                or next_direction == "RTL"
            ):
                result[index] = "RTL"

        return result

    @staticmethod
    def _get_direction(
        char: str,
    ) -> str:
        """Detect character direction."""

        if is_rtl_character(char):
            return "RTL"

        if (
            is_ltr_character(char)
            or is_number_character(char)
        ):
            return "LTR"

        return "NEUTRAL"
