from app.services.text_segment import TextSegment


def test_create_text_segment() -> None:
    segment = TextSegment(
        text="k-means",
        direction="LTR",
    )

    assert segment.text == "k-means"
    assert segment.direction == "LTR"
