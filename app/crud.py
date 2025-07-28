from sqlalchemy.orm import Session
from . import models, schemas, utils
from .utils import category_weight
from datetime import datetime
from app.database import SessionLocal
from sqlalchemy import func
import uuid

def create_submission(db: Session, data: schemas.SubmissionInput):
    base_score = utils.sigmoid_score(data.raw_value)
    weight = category_weight(data.category)
    weighted_score = min(round(base_score * weight, 2), 100.0)

    timestamp = datetime.utcnow()
    proof = utils.generate_proof(
        weighted_score, timestamp.isoformat(), data.verifier_id
    )

    submission = models.Submission(
        verifier_id=data.verifier_id,
        raw_value=data.raw_value,
        category=data.category,
        score=weighted_score,
        timestamp=timestamp,
        proof_of_score=proof,
    )
    db.add(submission)

    if weighted_score > 95:
        db.add(
            models.NotableImpact(
                verifier_id=data.verifier_id,
                raw_value=data.raw_value,
                category=data.category,
                score=weighted_score,
                timestamp=timestamp,
            )
        )

    db.commit()
    return submission


def get_submission(db: Session, submission_id):
    return (
        db.query(models.Submission)
        .filter(models.Submission.submission_id == submission_id)
        .first()
    )


def process_submission(data):
    db = SessionLocal()
    try:
        base_score = utils.sigmoid_score(data.raw_value)
        weight = utils.category_weight(data.category)
        weighted_score = min(round(base_score * weight, 2), 100.0)

        timestamp = datetime.utcnow()
        proof = utils.generate_proof(
            weighted_score, timestamp.isoformat(), data.verifier_id
        )

        submission = models.Submission(
            verifier_id=data.verifier_id,
            raw_value=data.raw_value,
            category=data.category,
            score=weighted_score,
            timestamp=timestamp,
            proof_of_score=proof,
        )
        db.add(submission)

        if weighted_score > 95:
            db.add(
                models.NotableImpact(
                    verifier_id=data.verifier_id,
                    raw_value=data.raw_value,
                    category=data.category,
                    score=weighted_score,
                    timestamp=timestamp,
                )
            )

        db.commit()
        return weighted_score, submission
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_impact_summary(db):
    total = db.query(func.count(models.Submission.submission_id)).scalar()

    # Group the data by category so that the average can be calculated within each group
    averages = (
        db.query(models.Submission.category, func.avg(models.Submission.score))
        .group_by(models.Submission.category)
        .all()
    )

    # Convert the list of tuples into a dictionary
    category_averages = {category: round(avg, 2) for category, avg in averages}

    return {"total_submissions": total, "average_score_by_category": category_averages}
