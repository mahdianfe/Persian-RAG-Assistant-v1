from app.services.pdf_structure import (
    PDFCharacter,
    PDFLine,
)

from app.services.text_direction import (
    is_rtl_character,
)

from app.services.text_normalizer import (
    PDFTextNormalizer,
)


class PDFReconstructionService:
    """Reconstruct text from PDF geometry."""

    @classmethod
    def reconstruct_line(
        cls,
        line: PDFLine,
    ) -> str:

        if not line.characters:
            return ""

        characters = cls._order_characters(
            line.characters,
        )

        text = cls._join_characters(
            characters,
        )

        return PDFTextNormalizer.normalize(
            text,
        )


    @classmethod
    def _order_characters(
        cls,
        characters: list[PDFCharacter],
    ) -> list[PDFCharacter]:

        has_rtl = any(
            is_rtl_character(c.text)
            for c in characters
        )

        has_ltr = any(
            not is_rtl_character(c.text)
            for c in characters
        )


        # Persian / Arabic only
        if has_rtl and not has_ltr:
            return sorted(
                characters,
                key=lambda c: c.x0,
                reverse=True,
            )


        # English only
        if has_ltr and not has_rtl:
            return sorted(
                characters,
                key=lambda c: c.x0,
            )


        # Mixed content:
        # keep original PDF order
        return characters


    @staticmethod
    def _join_characters(
        characters: list[PDFCharacter],
    ) -> str:

        result = []

        previous = None


        for current in characters:

            if previous is not None:

                if (
                    previous.text != " "
                    and current.text != " "
                ):

                    previous_rtl = is_rtl_character(
                        previous.text,
                    )

                    current_rtl = is_rtl_character(
                        current.text,
                    )


                    gap = 0


                    # RTL direction
                    if (
                        previous_rtl
                        and current_rtl
                    ):
                        gap = max(
                            previous.x0 -
                            current.x1,
                            0,
                        )


                    # LTR direction
                    elif (
                        not previous_rtl
                        and not current_rtl
                    ):
                        gap = max(
                            current.x0 -
                            previous.x1,
                            0,
                        )


                    # Word boundary detection
                    if (
                        gap >= 5
                        and (
                            not previous_rtl
                            or not current_rtl
                            or len(result) >= 3
                        )
                    ):
                        result.append(" ")


                    # RTL -> LTR transition
                    if (
                        previous_rtl
                        and not current_rtl
                    ):
                        if (
                            result
                            and result[-1] != " "
                        ):
                            result.append(" ")


            result.append(
                current.text,
            )

            previous = current


        return "".join(result)
