from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid


@dataclass
class DocumentRecord:
    doc_id: str
    filename: str
    full_text: str
    chunks: List[str]
    created_at: str  # ISO timestamp


# Simple in-memory store (resets when backend restarts)
_DOC_STORE: Dict[str, DocumentRecord] = {}


def save_document(filename: str, full_text: str, chunks: List[str]) -> str:
    """
    Save the document and its chunks in an in-memory store.

    Args:
        filename: Original uploaded filename.
        full_text: Full extracted text.
        chunks: List of chunk strings.

    Returns:
        A unique document id (doc_id).
    """
    if not filename:
        raise ValueError("filename is required")

    if not isinstance(full_text, str):
        raise TypeError("full_text must be a string")

    if not isinstance(chunks, list) or not all(isinstance(c, str) for c in chunks):
        raise TypeError("chunks must be a list of strings")

    doc_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    _DOC_STORE[doc_id] = DocumentRecord(
        doc_id=doc_id,
        filename=filename,
        full_text=full_text,
        chunks=chunks,
        created_at=created_at,
    )

    return doc_id


def get_document(doc_id: str) -> Optional[dict]:
    """
    Retrieve a document by id.

    Returns:
        dict with document data, or None if not found.
    """
    record = _DOC_STORE.get(doc_id)
    if record is None:
        return None

    # Return a plain dict (easy to JSON-serialize in routes)
    return {
        "doc_id": record.doc_id,
        "filename": record.filename,
        "full_text": record.full_text,
        "chunks": record.chunks,
        "chunk_count": len(record.chunks),
        "created_at": record.created_at,
    }
