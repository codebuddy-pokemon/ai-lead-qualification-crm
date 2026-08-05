from fastapi.testclient import TestClient

from app.main import app
from app.services.lead_store import lead_store

client = TestClient(app)


def valid_lead() -> dict[str, object]:
    return {
        "full_name": "Sarah Khan",
        "email": "sarah@exampleagency.com",
        "phone": "+1 555 010 2040",
        "job_title": "Operations Director",
        "company_name": "Example Agency",
        "website": "https://exampleagency.com",
        "industry": "Marketing services",
        "company_size": "11-50",
        "requested_service": "crm_automation",
        "problem_description": "Our team manually reviews every inbound lead and often follows up too late.",
        "budget_range": "5000_9999",
        "project_timeline": "within_30_days",
        "preferred_contact_method": "email",
        "consent_to_contact": True,
    }


def setup_function() -> None:
    lead_store.clear()


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
    "status": "healthy",
    "service": "lead-qualification-api",
}


def test_local_frontend_origin_is_allowed() -> None:
    response = client.options(
        "/api/v1/leads",
        headers={
            "Origin": "http://127.0.0.1:3000",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:3000"


def test_accepts_a_valid_lead() -> None:
    response = client.post("/api/v1/leads", json=valid_lead())

    assert response.status_code == 201
    assert response.json()["status"] == "submitted"
    assert response.json()["id"]
    assert lead_store.count() == 1


def test_rejects_an_invalid_email() -> None:
    lead = valid_lead()
    lead["email"] = "not-an-email"

    response = client.post("/api/v1/leads", json=lead)

    assert response.status_code == 422
    assert lead_store.count() == 0


def test_rejects_a_short_problem_description() -> None:
    lead = valid_lead()
    lead["problem_description"] = "Need AI."

    response = client.post("/api/v1/leads", json=lead)

    assert response.status_code == 422


def test_requires_phone_for_phone_contact() -> None:
    lead = valid_lead()
    lead["phone"] = None
    lead["preferred_contact_method"] = "phone"

    response = client.post("/api/v1/leads", json=lead)

    assert response.status_code == 422
