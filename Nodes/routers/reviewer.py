from fastapi import APIRouter
from datetime import datetime

from models.schemas import ReviewNote, AssignReviewer
from database import live_claims, reviewer_queue

router = APIRouter()


@router.post("/request-more-info/{claim_id}")
def request_more_info(claim_id: str):

    live_claims.update_one(
        {"claim_id": claim_id},
        {
            "$set": {
                "human_review.additional_info_requested": True,
                "human_review.requested_fields": ["repair_invoice", "medical_report"],
                "updated_at": datetime.utcnow(),
            }
        },
    )

    return {"message": "Additional information requested."}


@router.post("/reviewer/approve/{claim_id}")
def approve_claim(claim_id: str):

    live_claims.update_one(
        {"claim_id": claim_id},
        {
            "$set": {
                "workflow_status": "APPROVED_BY_REVIEWER",
                "updated_at": datetime.utcnow(),
            }
        },
    )

    reviewer_queue.delete_one({"claim_id": claim_id})

    return {"message": "Claim approved by reviewer"}


@router.post("/reviewer/reject/{claim_id}")
def reject_claim(claim_id: str):

    live_claims.update_one(
        {"claim_id": claim_id},
        {
            "$set": {
                "workflow_status": "REJECTED_BY_REVIEWER",
                "updated_at": datetime.utcnow(),
            }
        },
    )

    reviewer_queue.delete_one({"claim_id": claim_id})

    return {"message": "Claim rejected by reviewer"}


@router.post("/reviewer/add-note/{claim_id}")
def add_review_note(claim_id: str, review: ReviewNote):

    live_claims.update_one(
        {"claim_id": claim_id},
        {
            "$push": {
                "human_review.review_notes": {
                    "note": review.note,
                    "timestamp": datetime.utcnow(),
                }
            }
        },
    )

    return {"message": "Note added"}


@router.post("/reviewer/assign/{claim_id}")
def assign_reviewer(claim_id: str, data: AssignReviewer):

    reviewer_queue.update_one(
        {"claim_id": claim_id},
        {
            "$set": {
                "assigned_reviewer": data.reviewer_name,
                "status": "IN_REVIEW",
                "updated_at": datetime.utcnow(),
            }
        },
    )

    return {"message": "Reviewer assigned"}
