from app.services.chunking import TextChunkingService
from app.services.text import TextCleaningService


def test_text_cleaning() -> None:
    text = "سلام   دنیا\n\n\nاین   یک تست است"

    cleaned = TextCleaningService.clean(text)

    assert cleaned == "سلام دنیا\n\nاین یک تست است"


def test_repeated_title_is_removed() -> None:
    text = (
        "جزوه مقدماتی یادگیری ماشین\n"
        "پاراگراف اول درباره یادگیری ماشین.\n"
        "جزوه مقدماتی یادگیری ماشین\n"
        "پاراگراف دوم درباره رگرسیون.\n"
        "جزوه مقدماتی یادگیری ماشین\n"
        "پاراگراف سوم درباره طبقه بندی."
    )

    cleaned = TextCleaningService.clean(text)

    assert cleaned.count("جزوه مقدماتی یادگیری ماشین") == 1
    assert "پاراگراف اول درباره یادگیری ماشین." in cleaned
    assert "پاراگراف دوم درباره رگرسیون." in cleaned
    assert "پاراگراف سوم درباره طبقه بندی." in cleaned


def test_page_number_only_lines_are_removed() -> None:
    text = (
        "مقدمه\n"
        "1\n"
        "این متن درباره یادگیری ماشین است.\n"
        "2\n"
        "این متن درباره رگرسیون است."
    )

    cleaned = TextCleaningService.clean(text)

    assert "1" not in cleaned
    assert "2" not in cleaned
    assert "این متن درباره یادگیری ماشین است." in cleaned
    assert "این متن درباره رگرسیون است." in cleaned


def test_text_chunking() -> None:
    text = "abcdefghijklmnopqrstuvwxyz"

    service = TextChunkingService(
        chunk_size=10,
        chunk_overlap=3,
    )

    chunks = service.split(text)

    assert chunks == [
        "abcdefghij",
        "hijklmnopq",
        "opqrstuvwx",
        "vwxyz",
    ]


def test_paragraph_aware_chunking() -> None:
    text = (
        "پاراگراف اول درباره یادگیری ماشین است.\n\n"
        "پاراگراف دوم درباره رگرسیون است.\n\n"
        "پاراگراف سوم درباره طبقه بندی است."
    )

    service = TextChunkingService(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = service.split(text)

    assert len(chunks) == 2

    assert "پاراگراف اول درباره یادگیری ماشین است." in chunks[0]
    assert "پاراگراف دوم درباره رگرسیون است." in chunks[0]
    assert "پاراگراف سوم درباره طبقه بندی است." in chunks[1]


def test_paragraphs_are_not_broken_when_they_fit() -> None:
    text = (
        "این یک پاراگراف کوتاه است.\n\n"
        "این هم یک پاراگراف کوتاه دیگر است."
    )

    service = TextChunkingService(
        chunk_size=40,
        chunk_overlap=10,
    )

    chunks = service.split(text)

    assert len(chunks) >= 2
    assert chunks[0].strip()
    assert chunks[1].strip()


def test_large_paragraph_is_split() -> None:
    text = (
        "این یک جمله نسبتاً طولانی درباره یادگیری ماشین است. "
        "این جمله درباره داده و آموزش مدل صحبت می‌کند. "
        "این جمله درباره ارزیابی مدل صحبت می‌کند. "
        "این جمله درباره پیش‌بینی روی داده جدید صحبت می‌کند."
    )

    service = TextChunkingService(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = service.split(text)

    assert len(chunks) > 1

    for chunk in chunks:
        assert len(chunk) <= 100


def test_empty_text_returns_no_chunks() -> None:
    service = TextChunkingService()

    assert service.split("") == []


def test_invalid_chunk_configuration() -> None:
    try:
        TextChunkingService(
            chunk_size=100,
            chunk_overlap=100,
        )
    except ValueError as exc:
        assert str(exc) == (
            "chunk_overlap must be smaller than chunk_size."
        )
    else:
        raise AssertionError("Expected ValueError.")


def test_table_of_contents_page_is_removed() -> None:
    text = (
        "--- PAGE 1 ---\n"
        "جزوه مقدماتی یادگیری ماشین\n"
        "فهرست مطالب\n"
        "۱. مقدمه: چرا یادگیری ماشین اهمیت دارد\n"
        "۲. تعریف یادگیری ماشین\n"
        "--- PAGE 2 ---\n"
        "جزوه مقدماتی یادگیری ماشین\n"
        "۱. مقدمه: چرا یادگیری ماشین اهمیت دارد\n"
        "یادگیری ماشین یکی از مهم‌ترین زیرشاخه‌های هوش مصنوعی است."
    )

    cleaned = TextCleaningService.clean(text)

    assert "فهرست مطالب" not in cleaned
    assert "۲. تعریف یادگیری ماشین" not in cleaned
    assert "۱. مقدمه: چرا یادگیری ماشین اهمیت دارد" in cleaned
    assert (
        "یادگیری ماشین یکی از مهم ترین زیرشاخه های هوش مصنوعی است."
        in cleaned
    )


def test_section_aware_chunking() -> None:
    text = (
        "مقدمه\n"
        "یادگیری ماشین از داده ها الگو می آموزد.\n\n"
        "۲ .۱ مقدمه: چرا یادگیری ماشین اهمیت دارد\n"
        "این بخش درباره اهمیت یادگیری ماشین است.\n"
        "یادگیری ماشین در مسائل واقعی کاربرد دارد.\n\n"
        "۳ .۲ تعریف یادگیری ماشین و تفاوت آن با برنامه نویسی سنتی\n"
        "یادگیری ماشین از نمونه ها الگو می آموزد."
    )

    service = TextChunkingService(
        chunk_size=200,
        chunk_overlap=30,
    )

    chunks = service.split_sections(text)

    assert len(chunks) == 3

    assert "۲ .۱ مقدمه" in chunks[1]
    assert "اهمیت یادگیری ماشین" in chunks[1]

    assert "۳ .۲ تعریف یادگیری ماشین" in chunks[2]
    assert "از نمونه ها الگو می آموزد" in chunks[2]

def test_text_cleaning_removes_pdf_page_counter() -> None:
    text = """
جزوه مقدماتی یادگیری ماشین
1 / 1
مقدمه
یادگیری ماشین چیست؟
"""

    result = TextCleaningService.clean(text)

    assert "1 / 1" not in result

def test_text_cleaning_removes_pdf_filename() -> None:
    text = (
        "persian-rag-test-02.pdf\n"
        "جزوه مقدماتی یادگیری ماشین\n"
        "این متن درباره یادگیری ماشین است."
    )

    result = TextCleaningService.clean(text)

    assert "persian-rag-test-02" not in result
    assert ".pdf" not in result
    assert "این متن درباره یادگیری ماشین است." in result
