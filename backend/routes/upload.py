from fastapi import APIRouter, UploadFile, File, HTTPException
from services.pdf_extractor import validate_pdf, extract_text_from_pdf
from services.chunker import chunk_text
from services.doc_store import save_document

router = APIRouter(tags=["Upload"])


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # 1) Basic validation
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        validate_pdf(file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2) Extract text
    try:
        result = extract_text_from_pdf(file.file)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    text = result["text"] or ""
    preview = text[:800]

    # 3) Chunk + store
    chunks = chunk_text(text)
    doc_id = save_document(file.filename, text, chunks)

    # 4) Return response (now includes doc_id + chunk_count)
    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "num_pages": result["num_pages"],
        "text_length": len(text),
        "chunk_count": len(chunks),
        "preview": preview,
        "warnings": result["warnings"],
    }
