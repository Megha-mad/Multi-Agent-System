"""Starter PDF ingestion and page-wise text extraction (PyMuPDF).

Status: starter implementation. OCR for scanned pages is not implemented yet;
such pages are flagged with a warning instead.
"""
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path

import pymupdf as fitz  # PyMuPDF

ALLOWED_EXTENSIONS = {".pdf"}
PDF_MAGIC = b"%PDF"


class PDFValidationError(Exception):
    """Raised when the uploaded file is not a readable PDF."""


@dataclass
class PageResult:
    document_id: str
    page_number: int          # 1-based, matches the original PDF
    page_text: str
    extraction_method: str    # "text" or "ocr"
    status: str               # "success" or "failure"
    warnings: list = field(default_factory=list)


def validate_pdf(path: str) -> Path:
    p = Path(path)
    if p.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise PDFValidationError(f"Unsupported file format: {p.suffix}")
    if not p.is_file():
        raise PDFValidationError("File not found")
    with open(p, "rb") as f:
        if f.read(4) != PDF_MAGIC:
            raise PDFValidationError("File is not a valid PDF (bad header)")
    return p


def new_document_id() -> str:
    return uuid.uuid4().hex


def extract_pages(path: str, document_id: str | None = None) -> list[dict]:
    """Extract text page by page, keeping original page numbers."""
    p = validate_pdf(path)
    document_id = document_id or new_document_id()
    try:
        doc = fitz.open(p)
    except Exception as exc:
        raise PDFValidationError(f"Unreadable or corrupted PDF: {exc}") from exc

    results = []
    with doc:
        if doc.needs_pass:
            raise PDFValidationError("PDF is password protected")
        for index, page in enumerate(doc, start=1):
            try:
                text = page.get_text("text").strip()
                if text:
                    r = PageResult(document_id, index, text, "text", "success")
                else:
                    r = PageResult(
                        document_id, index, "", "text", "failure",
                        ["Empty page or scanned image; OCR required"],
                    )
            except Exception as exc:
                r = PageResult(document_id, index, "", "text", "failure",
                               [f"Extraction error: {exc}"])
            results.append(asdict(r))
    return results


if __name__ == "__main__":
    import json
    import sys

    print(json.dumps(extract_pages(sys.argv[1]), indent=2, ensure_ascii=False))
