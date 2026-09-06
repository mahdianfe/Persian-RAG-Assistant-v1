class ExtractionService:

    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize text for term matching.
        """

        text = text.lower()

        replacements = {
            "‌": "",
            " ": "",
            "-": "",
            "_": "",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text


    @staticmethod
    def extract_terms(
        question: str,
        context: str,
    ) -> str | None:

        question_lower = question.lower()

        normalized_context = (
            ExtractionService._normalize(context)
        )


        # استخراج الگوریتم‌ها
        if "الگوریتم" in question_lower:

            results = []

            terms = [
                "Regression",
                "Classification",
                "k-means",
                "Clustering",
            ]

            for term in terms:

                normalized_term = (
                    ExtractionService._normalize(term)
                )

                if normalized_term in normalized_context:
                    results.append(term)


            if results:
                return "\n".join(results)


        # استخراج واژه‌ها و نام‌ها
        if (
            "واژه" in question_lower
            or "نام" in question_lower
            or "ابزار" in question_lower
        ):

            results = []

            terms = [
                "Python",
                "RAG",
                "PDF",
                "scikit-learn",
            ]

            for term in terms:

                normalized_term = (
                    ExtractionService._normalize(term)
                )

                if normalized_term in normalized_context:
                    results.append(term)


            if results:
                return "\n".join(results)


        return None
