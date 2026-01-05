from fastapi import APIRouter, HTTPException
from schemas.study import StudyRequest, StudyResponse
from services.doc_store import get_document

router = APIRouter(prefix="/study", tags=["Study"])


@router.post("/", response_model=StudyResponse)
async def study(req: StudyRequest):
    # 1) Fetch doc
    doc = get_document(req.doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")

    # 2) Choose chunks + combine
    chunks = doc["chunks"]
    selected_chunks = chunks[:4]   # or [:6]
    selected_text = "\n\n".join(selected_chunks)

    # 3) Make output differ by mode (placeholder ok)
    if req.mode.value == "summarize":
        output = (
            "📝 Summary (placeholder)\n"
            f"Using {len(selected_chunks)} chunks from '{doc['filename']}'.\n\n"
            f"Text preview:\n{selected_text[:500]}..."
        )

    elif req.mode.value == "explain":
        focus = req.focus or "the main ideas"
        output = (
            "📘 Explanation (placeholder)\n"
            f"Focus: {focus}\n"
            f"Using {len(selected_chunks)} chunks from '{doc['filename']}'.\n\n"
            f"Text preview:\n{selected_text[:500]}..."
        )

    elif req.mode.value == "quiz":
        output = (
            "🧠 Quiz (placeholder)\n"
            f"Questions: {req.num_questions}\n"
            f"Difficulty: {req.difficulty}\n"
            f"Using {len(selected_chunks)} chunks from '{doc['filename']}'.\n\n"
            "Example Q1 (placeholder): What is one key idea mentioned in the text?"
        )

    else:
        # Shouldn't happen if your Pydantic enum is correct, but safe fallback
        raise HTTPException(status_code=400, detail="Invalid mode")

    print(
        f"[study] doc_id={req.doc_id} mode={req.mode.value} "
        f"selected_chunks={len(selected_chunks)}"
    )

    # 4) Return correct StudyResponse (Step 2.2.5)
    return StudyResponse(
        doc_id=req.doc_id,
        mode=req.mode.value,
        output=output,
        used_chunks=len(selected_chunks),
        warnings=[]
    )
