from fastapi import APIRouter, HTTPException
from services.doc_store import get_document

router = APIRouter(tags=["Docs"])


@router.get("/docs/{doc_id}")
def read_doc(doc_id: str):
    doc = get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="doc_id not found")

    chunks = doc.get("chunks", [])
    return {
        "doc_id": doc["doc_id"],
        "filename": doc["filename"],
        "created_at": doc["created_at"],
        "chunk_count": len(chunks),
        "chunks_preview": chunks[:2],  # only return first 2 chunks
    }
