from fastapi import APIRouter, UploadFile, File, HTTPException
from services.pdf_extractor import validate_pdf, extract_text_from_pdf


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
        # NOTE: UploadFile.file is a file-like object that PdfReader can read
        result = extract_text_from_pdf(file.file)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    text = result["text"] or ""
    preview = text[:800]  # keep it short for Phase 1

    return {
        "filename": file.filename,
        "num_pages": result["num_pages"],
        "text_length": len(text),
        "preview": preview,
        "warnings": result["warnings"],
    }
