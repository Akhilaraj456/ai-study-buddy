from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


# 1) StudyMode enum (only these string values are allowed)
class StudyMode(str, Enum):
    summarize = "summarize"
    quiz = "quiz"
    explain = "explain"


# 2) Request model (what the client sends to POST /study)
class StudyRequest(BaseModel):
    doc_id: str = Field(..., description="Document ID to study (from your stored docs)")
    mode: StudyMode = Field(..., description="summarize | quiz | explain")

    focus: Optional[str] = Field(
        default=None,
        description='Optional topic focus, e.g. "integration by parts"'
    )

    num_questions: int = Field(
        default=8,
        ge=1,
        le=50,
        description="Only used for quiz mode. Default 8."
    )

    difficulty: str = Field(
        default="mixed",
        pattern="^(easy|medium|hard|mixed)$",
        description="easy | medium | hard | mixed"
    )


# 3) Response model (what your API returns)
class StudyResponse(BaseModel):
    doc_id: str
    mode: str
    output: str
    used_chunks: int
    warnings: List[str] = Field(default_factory=list)
