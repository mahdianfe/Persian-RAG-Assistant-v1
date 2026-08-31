import unicodedata


def is_rtl_character(char: str) -> bool:
    """
    Check whether character belongs to RTL scripts.
    """

    if not char:
        return False

    direction = unicodedata.bidirectional(char)

    return direction in {
        "R",
        "AL",
    }


def is_ltr_character(char: str) -> bool:
    """
    Check whether character belongs to LTR scripts.
    """

    if not char:
        return False

    direction = unicodedata.bidirectional(char)

    return direction == "L"


def is_number_character(char: str) -> bool:
    """
    Check numeric characters.
    """

    if not char:
        return False

    return char.isdigit()
