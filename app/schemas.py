from pydantic import BaseModel, Field, StrictFloat
from uuid import UUID
from datetime import datetime
from typing import List, Dict, Literal


class SubmissionInput(BaseModel):
    verifier_id: str
    raw_value: StrictFloat = Field(
        ..., gt=0, lt=1_000_000, description="Must be a positive number"
    )
    category: Literal["emissions", "water", "waste"]


class SubmissionResponse(BaseModel):
    submission_id: UUID
    score: float
    proof_of_score: str


class ScoreResponse(BaseModel):
    submission_id: UUID
    score: float
    proof_of_score: str
    timestamp: datetime


class BatchSubmitResponse(BaseModel):
    total_submissions: int
    average_score: float
    distribution: Dict[str, int]


class ImpactSummary(BaseModel):
    total_submissions: int
    average_score_by_category: Dict[str, float]
