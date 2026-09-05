import re


class AnswerValidator:
    """Validate that answer is grounded in context."""

    @staticmethod
    def validate(
        answer: str,
        context: str,
    ) -> str:
        """
        Reject answers containing unsupported information.
        """

        answer_words = set(
            re.findall(
                r"\w+",
                answer.lower(),
            )
        )

        context_words = set(
            re.findall(
                r"\w+",
                context.lower(),
            )
        )

        unsupported = (
            answer_words - context_words
        )

        # Ignore common Persian response words
        ignored = {
            "است",
            "در",
            "این",
            "و",
            "به",
            "از",
            "های",
            "که",
        }

        unsupported -= ignored

        if len(unsupported) > 5:
            return (
                "پاسخ این سؤال در اسناد موجود پیدا نشد."
            )

        return answer
