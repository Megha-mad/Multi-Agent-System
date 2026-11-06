import pytest
import pymupdf as fitz

from src.extractor import extract_pages, PDFValidationError


def make_pdf(path, pages):
    doc = fitz.open()
    for text in pages:
        page = doc.new_page()
        if text:
            page.insert_text((72, 72), text)
    doc.save(path)
    doc.close()


def test_page_numbers_and_numbers_preserved(tmp_path):
    f = tmp_path / "report.pdf"
    make_pdf(f, ["Revenue: Rs. 1,234.56 crore", "Net profit: $98.76 million"])
    res = extract_pages(str(f))
    assert [r["page_number"] for r in res] == [1, 2]
    assert "1,234.56" in res[0]["page_text"]
    assert "$98.76" in res[1]["page_text"]


def test_empty_page_flagged(tmp_path):
    f = tmp_path / "empty.pdf"
    make_pdf(f, ["Some text", ""])
    res = extract_pages(str(f))
    assert res[1]["status"] == "failure" and res[1]["warnings"]


def test_rejects_non_pdf(tmp_path):
    f = tmp_path / "notes.txt"
    f.write_text("hello")
    with pytest.raises(PDFValidationError):
        extract_pages(str(f))


def test_rejects_corrupted_pdf(tmp_path):
    f = tmp_path / "bad.pdf"
    f.write_bytes(b"not a pdf at all")
    with pytest.raises(PDFValidationError):
        extract_pages(str(f))
