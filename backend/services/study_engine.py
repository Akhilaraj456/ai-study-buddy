from services.llm_client import chat_completion
from __future__ import annotations
from typing import List, Optional, Tuple
from schemas.study import StudyMode

import re
from typing import List, Optional


def select_relevant_chunks(
    chunks: List[str],
    focus: Optional[str],
    max_chunks: int = 3,
) -> List[str]:
    """
    Simple keyword-based retrieval.
    Scores chunks by keyword overlap with focus.
    """
    if not focus:
        return chunks[:max_chunks]

    keywords = [
        w.lower() for w in re.findall(r"\w+", focus) if len(w) > 2
    ]

    if not keywords:
        return chunks[:max_chunks]

    scored = []
    for chunk in chunks:
        text = chunk.lower()
        score = sum(text.count(k) for k in keywords)
        if score > 0:
            scored.append((score, chunk))

    # Sort by relevance score (descending)
    scored.sort(reverse=True, key=lambda x: x[0])

    selected = [chunk for _, chunk in scored[:max_chunks]]

    # Fallback if nothing matched
    if not selected:
        return chunks[:max_chunks]

    return selected

def build_prompt(
    mode: StudyMode,
    focus: Optional[str],
    chunks: List[str],
    num_questions: int = 8,
    difficulty: str = "mixed",
    max_chunks: int = 3,
) -> Tuple[str, int]:
    """
    Build a prompt-like string from the first N chunks.
    Returns (prompt, used_chunks).
    """
    from services.study_engine import select_relevant_chunks  # if same file, just call directly

    selected = select_relevant_chunks(
        chunks=chunks,
        focus=focus,
        max_chunks=max_chunks,
)
    used_chunks = len(selected)

    context = "\n\n---\n\n".join(selected)

    focus_line = f"Focus topic: {focus}\n" if focus else ""
    header = (
        f"You are an AI Study Buddy.\n"
        f"Task: {mode.value}\n"
        f"{focus_line}"
        f"Difficulty: {difficulty}\n"
    )

    if mode == StudyMode.quiz:
        header += f"Number of questions: {num_questions}\n"

    prompt = header + "\nContext:\n" + context
    return prompt, used_chunks


def run_study_mode(
    mode: StudyMode,
    focus: Optional[str],
    chunks: List[str],
    num_questions: int = 8,
    difficulty: str = "mixed",
) -> Tuple[str, int]:
    prompt, used_chunks = build_prompt(
        mode=mode,
        focus=focus,
        chunks=chunks,
        num_questions=num_questions,
        difficulty=difficulty,
        max_chunks=3,
    )

    if mode == StudyMode.summarize:
        output = (
            "📝 Summary\n"
            "- Key idea 1\n"
            "- Key idea 2\n"
            "- Key idea 3\n\n"
            "Context preview used:\n"
            f"{prompt[:500]}..."
        )
        return output, used_chunks

    if mode == StudyMode.explain:
        topic = focus or "the main ideas"
        output = (
            f"📘 Explanation — {topic}\n"
            "1) What it is: ...\n"
            "2) Why it matters: ...\n"
            "3) Common mistakes: ...\n"
            "4) Mini example: ...\n\n"
            "Context preview used:\n"
            f"{prompt[:500]}..."
        )
        return output, used_chunks

    # quiz
    questions = [f"{i+1}. ({difficulty}) Question {i+1} based on the PDF text..." for i in range(num_questions)]
    output = "🧠 Quiz\n" + "\n".join(questions)
    return output, used_chunks

