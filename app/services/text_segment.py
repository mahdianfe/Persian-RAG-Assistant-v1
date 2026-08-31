from dataclasses import dataclass


@dataclass
class TextSegment:
    """
    A continuous text segment with one direction.
    """

    text: str
    direction: str
