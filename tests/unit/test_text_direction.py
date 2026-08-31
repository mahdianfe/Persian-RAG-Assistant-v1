from app.services.text_direction import (
    is_ltr_character,
    is_number_character,
    is_rtl_character,
)


def test_persian_character_is_rtl() -> None:
    assert is_rtl_character("م")


def test_english_character_is_ltr() -> None:
    assert is_ltr_character("k")


def test_number_character() -> None:
    assert is_number_character("1")
