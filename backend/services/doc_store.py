# backend/services/doc_store.py

from __future__ import annotations
from typing import Dict, Any, Optional
import uuid

# Module-level "in-memory DB"
# Key: doc_id (str)
# Value: dict with filename, full_text, chunks, optional num_pages
_DOC_STORE: Dict[str, Dict[str, Any]] = {}


def save_document(
    filename: str,
    full_text: str,
    chunks: list[str],
    num_pages: int | None = None,
) -> str:
    """
    Save a processed document in memory and return a unique doc_id.
    """
    doc_id = str(uuid.uuid4())

    doc: Dict[str, Any] = {
        "doc_id": doc_id,
        "filename": filename,
        "full_text": full_text,
        "chunks": chunks,
    }

    if num_pages is not None:
        doc["num_pages"] = num_pages

    _DOC_STORE[doc_id] = doc
    return doc_id


def get_document(doc_id: str) -> Optional[Dict[str, Any]]:
    """
    Return the stored document dict, or None if not found.
    """
    return _DOC_STORE.get(doc_id)


def clear_store() -> None:
    """
    Optional helper for debugging/tests.
    """
    _DOC_STORE.clear()
