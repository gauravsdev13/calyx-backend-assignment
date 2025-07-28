# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from typing import List
from app.utils import score_bucket
from app.schemas import BatchSubmitResponse, ImpactSummary
from app.crud import get_impact_summary
import asyncio
import logging


logging.basicConfig(
    level=logging.INFO,
    filename="calyx_backend.log",
    format="%(asctime)s [%(levelname)s] %(message)s",
)


logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/submit", response_model=schemas.SubmissionResponse)
def submit(data: schemas.SubmissionInput, db: Session = Depends(get_db)):
    try:
        submission = crud.create_submission(db, data)
        logger.info(
            f"Submission received from {data.verifier_id} with raw_value={data.raw_value} → score={submission.score}"
        )
        return {
            "submission_id": submission.submission_id,
            "score": submission.score,
            "proof_of_score": submission.proof_of_score,
        }
    except Exception as e:
        logger.exception("Error during submission")
        raise HTTPException(status_code=500, detail="Submission failed")


@app.get("/score/{submission_id}", response_model=schemas.ScoreResponse)
def get_score(submission_id: UUID, db: Session = Depends(get_db)):
    try:
        submission = crud.get_submission(db, submission_id)
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")
        return submission
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error retrieving score")
        raise HTTPException(status_code=500, detail="Failed to retrieve score")


@app.post("/batch-submit", response_model=schemas.BatchSubmitResponse)
async def batch_submit(
    submissions: List[schemas.SubmissionInput], db: Session = Depends(get_db)
):
    try:
        # Process each submission concurrently
        tasks = [
            asyncio.to_thread(crud.process_submission, data) for data in submissions
        ]

        # Gather results when all tasks are complete
        processed = await asyncio.gather(*tasks)

        scores = []
        for score, _ in processed:
            scores.append(score)


        distribution = {"0–50": 0, "51–75": 0, "76–100": 0}
        for s in scores:
            distribution[score_bucket(s)] += 1

        avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0

        logger.info(
            f"Batch processed: {len(scores)} submissions, avg={avg_score}, dist={distribution}"
        )

        return BatchSubmitResponse(
            total_submissions=len(scores),
            average_score=avg_score,
            distribution=distribution,
        )

    except Exception as e:
        logger.exception("Error during batch processing")
        raise HTTPException(status_code=500, detail="Batch processing failed")


@app.get("/impact-summary", response_model=ImpactSummary)
def impact_summary(db: Session = Depends(get_db)):
    return get_impact_summary(db)
