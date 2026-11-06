# PDF Ingestion and Text Extraction Design

**Project:** Multi-Agent Financial Research System
**Batch:** CSM-B12
**Assigned member:** Mungara Meghana

## 1. Objective
Design a process for uploading financial PDF documents and extracting their text while preserving page information for accurate citations.

## 2. Proposed Workflow
1. User uploads a financial PDF.
2. Validate the file format.
3. Assign a unique document ID.
4. Store the uploaded PDF.
5. Extract text page by page.
6. Preserve page numbers.
7. Identify empty or unreadable pages.
8. Pass extracted text to the chunking module.

## 3. Proposed Technologies
- Python
- PyMuPDF
- FastAPI
- OCR tools for scanned PDFs, if required

## 4. Extraction Output
| Field | Description |
|---|---|
| Document ID | Unique document ID |
| Page Number | Original PDF page |
| Page Text | Extracted text |
| Extraction Method | Text extraction or OCR |
| Status | Success or failure |
| Warnings | Extraction problems |

## 5. Validation
Test for:
- Normal PDF documents
- Scanned PDF documents
- Corrupted PDFs
- Empty pages
- Financial tables
- Numbers, decimal values and currencies

Extracted text should be compared with the original PDF pages.

## 6. Error Handling
- Reject unsupported file formats.
- Handle unreadable PDFs.
- Detect empty pages.
- Preserve original page numbering.
- Report extraction errors clearly.
- Avoid uploading private documents or credentials to GitHub.

## 7. Expected Output
The extraction module provides page-wise text and metadata to the document chunking module.

## 8. Current Status
Proposed design with a starter implementation (`src/extractor.py`). Full testing with sample financial reports and OCR support are pending.

## 9. Next Steps
- Test PyMuPDF with sample financial reports.
- Implement PDF validation.
- Develop page-wise extraction.
- Test extraction quality.
- Document limitations and test results.
