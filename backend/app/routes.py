from fastapi import APIRouter, status

from app.models.lead import LeadAccepted, LeadCreate
from app.services.lead_qualifier import qualify_lead
from app.services.lead_store import lead_store

router = APIRouter()


@router.get("/health", tags=["Operations"])
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "lead-qualification-api",
    }


@router.post(
    "/api/v1/leads",
    response_model=LeadAccepted,
    status_code=status.HTTP_201_CREATED,
    tags=["Leads"],
)
def create_lead(lead: LeadCreate) -> LeadAccepted:
    qualification = qualify_lead(lead)
    accepted = LeadAccepted.from_submission(qualification=qualification)

    lead_store.save(
        lead_id=accepted.id,
        data=lead,
        received_at=accepted.received_at,
        qualification=qualification,
    )

    return accepted