# app/models.py
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .database import Base


class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    verifier_id = Column(String, nullable=False)
    raw_value = Column(Float, nullable=False)
    score = Column(Float, nullable=False)
    proof_of_score = Column(String, nullable=False)
    category = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class NotableImpact(Base):
    __tablename__ = "notable_impact"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    verifier_id = Column(String, nullable=False)
    raw_value = Column(Float, nullable=False)
    score = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
