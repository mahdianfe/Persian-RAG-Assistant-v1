from app.services.pdf_structure import (
    PDFCharacter,
    PDFLine,
)
from app.services.text_direction import (
    is_ltr_character,
    is_rtl_character,
)
from app.services.text_normalizer import (
    PDFTextNormalizer,
)


class PDFReconstructionService:
    """Reconstruct text from PDF character geometry."""

    MIN_WORD_GAP = 5.0
    BASELINE_MARGIN = 2.0

    @classmethod
    def reconstruct_line(
        cls,
        line: PDFLine,
    ) -> str:
        """Reconstruct one PDF line."""

        if not line.characters:
            return ""

        characters = cls._order_characters(
            line.characters,
        )

        text = cls._join_characters(
            characters,
        )

        print("BEFORE NORMALIZE:", repr(text))

        return PDFTextNormalizer.normalize(
            text,
        )

    @classmethod
    def _order_characters(
        cls,
        characters: list[PDFCharacter],
    ) -> list[PDFCharacter]:
        """
        Order characters using direction and PDF geometry.

        Pure RTL lines are ordered right-to-left.
        Pure LTR lines are ordered left-to-right.

        Mixed lines are first divided into directional runs.
        Those runs are then placed in logical order according to
        their horizontal geometry.
        """

        if not characters:
            return []

        has_rtl = any(
            is_rtl_character(character.text)
            for character in characters
        )

        has_ltr = any(
            is_ltr_character(character.text)
            for character in characters
        )

        if has_rtl and not has_ltr:
            return sorted(
                characters,
                key=lambda character: character.x0,
                reverse=True,
            )

        if has_ltr and not has_rtl:
            return sorted(
                characters,
                key=lambda character: character.x0,
            )

        return cls._order_mixed_characters(
            characters,
        )

    @classmethod
    def _order_mixed_characters(
        cls,
        characters: list[PDFCharacter],
    ) -> list[PDFCharacter]:
        """
        Reconstruct mixed RTL/LTR text.

        PDF extraction may return runs in visual / content-stream order.

        For example, the rendered line:

            این سند ... RAG فارسی ساخته شده است.

        can be extracted internally as approximately:

            . فارسی ساخته شده است RAG این سند ...

        We therefore reconstruct the order of directional runs using
        their horizontal positions before reconstructing each run.
        """

        runs = cls._split_direction_runs(
            characters,
        )

        ordered_runs = cls._order_runs_by_geometry(
            runs,
        )

        ordered: list[PDFCharacter] = []

        for run in ordered_runs:
            direction = cls._run_direction(
                run,
            )

            if direction == "rtl":
                ordered.extend(
                    cls._order_rtl_run(
                        run,
                    )
                )
                continue

            if direction == "ltr":
                ordered.extend(
                    cls._order_ltr_run(
                        run,
                    )
                )
                continue

            ordered.extend(run)

        return ordered

    @classmethod
    def _split_direction_runs(
        cls,
        characters: list[PDFCharacter],
    ) -> list[list[PDFCharacter]]:
        """
        Split extracted characters into directional runs.

        Neutral characters such as whitespace and punctuation remain
        attached to the current run when possible.

        This prevents punctuation such as the hyphen in
        ``scikit-learn`` from unnecessarily splitting an LTR token.
        """

        if not characters:
            return []

        runs: list[list[PDFCharacter]] = []

        current_run: list[PDFCharacter] = []
        current_direction: str | None = None

        for character in characters:
            direction = cls._character_direction(
                character,
            )

            if direction == "neutral":
                current_run.append(
                    character,
                )
                continue

            if not current_run:
                current_run.append(
                    character,
                )
                current_direction = direction
                continue

            if current_direction is None:
                current_run.append(
                    character,
                )
                current_direction = direction
                continue

            if direction == current_direction:
                current_run.append(
                    character,
                )
                continue

            runs.append(
                current_run,
            )

            current_run = [
                character,
            ]
            current_direction = direction

        if current_run:
            runs.append(
                current_run,
            )

        return runs

    @classmethod
    def _order_runs_by_geometry(
        cls,
        runs: list[list[PDFCharacter]],
    ) -> list[list[PDFCharacter]]:
        """
        Convert visual run placement to logical run order.
        """

        if len(runs) < 2:
            return list(runs)

        base_direction = cls._detect_base_direction(
            runs,
        )

        if base_direction == "rtl":

            first_run_direction = cls._run_direction(
                runs[0],
            )

            if first_run_direction == "ltr":

                first_run_text = "".join(
                    character.text
                    for character in runs[0]
                ).strip()

                # Short English tokens inside Persian sentences
                # should move to the end.
                if len(first_run_text) <= 6:
                    return sorted(
                        runs,
                        key=cls._run_center_x,
                        reverse=True,
                    )

                # Longer English prefixes stay at the beginning.
                return sorted(
                    runs,
                    key=cls._run_center_x,
                )

            return sorted(
                runs,
                key=cls._run_center_x,
                reverse=True,
            )

        if base_direction == "ltr":
            return sorted(
                runs,
                key=cls._run_center_x,
            )

        return list(runs)


    @classmethod
    def _detect_base_direction(
        cls,
        runs: list[list[PDFCharacter]],
    ) -> str:
        """
        Detect the base direction using the rightmost directional run.

        In a horizontal RTL line, the logical beginning of the line is
        normally located on the right side.

        In a horizontal LTR line, the rightmost directional run remains
        LTR.
        """

        directional_runs: list[
            tuple[list[PDFCharacter], str]
        ] = []

        for run in runs:
            direction = cls._run_direction(
                run,
            )

            if direction == "neutral":
                continue

            directional_runs.append(
                (
                    run,
                    direction,
                )
            )

        if not directional_runs:
            return "neutral"

        rightmost_run, direction = max(
            directional_runs,
            key=lambda item: cls._run_right_edge(
                item[0],
            ),
        )

        del rightmost_run

        return direction

    @staticmethod
    def _run_left_edge(
        run: list[PDFCharacter],
    ) -> float:
        """Return the left edge of a directional run."""

        return min(
            character.x0
            for character in run
        )

    @staticmethod
    def _run_right_edge(
        run: list[PDFCharacter],
    ) -> float:
        """Return the right edge of a directional run."""

        return max(
            character.x1
            for character in run
        )

    @classmethod
    def _run_center_x(
        cls,
        run: list[PDFCharacter],
    ) -> float:
        """Return horizontal center of a directional run."""

        left = cls._run_left_edge(
            run,
        )

        right = cls._run_right_edge(
            run,
        )

        return (
            left + right
        ) / 2.0

    @staticmethod
    def _character_direction(
        character: PDFCharacter,
    ) -> str:
        """Return rtl, ltr, or neutral."""

        text = character.text

        if not text:
            return "neutral"

        if is_rtl_character(
            text,
        ):
            return "rtl"

        if is_ltr_character(
            text,
        ):
            return "ltr"

        return "neutral"

    @classmethod
    def _run_direction(
        cls,
        run: list[PDFCharacter],
    ) -> str:
        """Return direction of the first meaningful character."""

        for character in run:
            direction = cls._character_direction(
                character,
            )

            if direction != "neutral":
                return direction

        return "neutral"

    @staticmethod
    def _order_rtl_run(
        run: list[PDFCharacter],
    ) -> list[PDFCharacter]:
        """
        Order a RTL run from right to left.

        Neutral characters that belong to the run are positioned
        according to their PDF geometry as well.
        """

        return sorted(
            run,
            key=lambda character: character.x0,
            reverse=True,
        )

    @staticmethod
    def _order_ltr_run(
        run: list[PDFCharacter],
    ) -> list[PDFCharacter]:
        """
        Preserve extracted logical order of an embedded LTR run.

        PyMuPDF can provide an English token in correct logical order
        even when its x coordinates decrease inside an RTL context.

        Therefore an embedded token such as:

            scikit-learn

        must not be reversed merely because its x coordinates decrease.
        """

        return list(run)

    @classmethod
    def _join_characters(
        cls,
        characters: list[PDFCharacter],
    ) -> str:
        """Join ordered characters and infer missing word spaces."""

        if not characters:
            return ""

        rtl_threshold = cls._calculate_gap_threshold(
            characters,
            direction="rtl",
        )

        ltr_threshold = cls._calculate_gap_threshold(
            characters,
            direction="ltr",
        )

        result: list[str] = []

        previous: PDFCharacter | None = None

        for current in characters:
            text = current.text

            if not text:
                continue

            if text.isspace():
                if (
                    result
                    and not result[-1].isspace()
                ):
                    result.append(
                        " ",
                    )

                previous = current
                continue

            if previous is not None:
                if cls._needs_space(
                    previous=previous,
                    current=current,
                    rtl_threshold=rtl_threshold,
                    ltr_threshold=ltr_threshold,
                ):
                    if (
                        result
                        and not result[-1].isspace()
                    ):
                        result.append(
                            " ",
                        )

            result.append(
                text,
            )

            previous = current

        return "".join(
            result,
        )

    @classmethod
    def _calculate_gap_threshold(
        cls,
        characters: list[PDFCharacter],
        direction: str,
    ) -> float:
        """
        Calculate an adaptive same-direction word-gap threshold.

        Some PDF fonts have a non-zero normal gap between every
        character. A fixed threshold would incorrectly convert those
        character gaps into word spaces.

        We therefore compare candidate gaps with the normal baseline
        spacing observed on the same line.
        """

        gaps: list[float] = []

        previous: PDFCharacter | None = None

        for current in characters:
            if previous is None:
                previous = current
                continue

            previous_direction = cls._character_direction(
                previous,
            )

            current_direction = cls._character_direction(
                current,
            )

            if (
                previous_direction != direction
                or current_direction != direction
            ):
                previous = current
                continue

            gap = cls._same_direction_gap(
                previous,
                current,
                direction,
            )

            if gap >= 0:
                gaps.append(
                    gap,
                )

            previous = current

        if not gaps:
            return cls.MIN_WORD_GAP

        baseline = min(
            gaps,
        )

        if baseline >= cls.MIN_WORD_GAP:
            return (
                baseline
                + cls.BASELINE_MARGIN
            )

        return cls.MIN_WORD_GAP

    @staticmethod
    def _same_direction_gap(
        previous: PDFCharacter,
        current: PDFCharacter,
        direction: str,
    ) -> float:
        """Return the geometric gap between same-direction characters."""

        if direction == "rtl":
            return max(
                previous.x0
                - current.x1,
                0.0,
            )

        return max(
            current.x0
            - previous.x1,
            0.0,
        )

    @classmethod
    def _needs_space(
        cls,
        previous: PDFCharacter,
        current: PDFCharacter,
        rtl_threshold: float,
        ltr_threshold: float,
    ) -> bool:
        """Return True when geometry indicates a missing word space."""

        if previous.text.isspace():
            return False

        if current.text.isspace():
            return False

        previous_direction = cls._character_direction(
            previous,
        )

        current_direction = cls._character_direction(
            current,
        )

        if (
            previous_direction == "neutral"
            or current_direction == "neutral"
        ):
            return False

        if (
            previous_direction == "rtl"
            and current_direction == "rtl"
        ):
            gap = cls._same_direction_gap(
                previous,
                current,
                "rtl",
            )

            return gap >= rtl_threshold

        if (
            previous_direction == "ltr"
            and current_direction == "ltr"
        ):
            gap = cls._same_direction_gap(
                previous,
                current,
                "ltr",
            )

            return gap >= ltr_threshold

        # Changing direction represents a token boundary when there
        # is no explicit whitespace character in the extracted stream.
        return True
