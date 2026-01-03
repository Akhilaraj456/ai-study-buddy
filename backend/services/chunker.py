# backend/services/chunker.py

from __future__ import annotations

import re


def chunk_text(text: str, max_chars: int = 1200, overlap: int = 150) -> list[str]:
    """
    Split text into overlapping character chunks.

    - Normalizes whitespace for cleaner downstream LLM inputs
    - Uses sliding window with overlap for context continuity

    Args:
        text: Input text to chunk.
        max_chars: Target max characters per chunk.
        overlap: Number of characters repeated between consecutive chunks.

    Returns:
        List of non-empty chunk strings.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if max_chars <= 0:
        raise ValueError("max_chars must be > 0")

    if overlap < 0:
        raise ValueError("overlap must be >= 0")

    if overlap >= max_chars:
        raise ValueError("overlap must be smaller than max_chars")

    # Basic whitespace normalization:
    # - turn Windows newlines into \n
    # - collapse 3+ newlines into 2
    # - collapse repeated spaces/tabs
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    normalized = re.sub(r"[ \t]{2,}", " ", normalized)
    normalized = normalized.strip()

    if not normalized:
        return []

    chunks: list[str] = []
    start = 0
    n = len(normalized)
    step = max_chars - overlap

    while start < n:
        end = min(start + max_chars, n)
        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= n:
            break

        start += step

    return chunks
