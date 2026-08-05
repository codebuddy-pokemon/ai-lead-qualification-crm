from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, model_validator


class CompanySize(str, Enum):
    SOLO = "1"
    SMALL = "2-10"
    GROWING = "11-50"
    MID_MARKET = "51-200"
    LARGE = "201-1000"
    ENTERPRISE = "1000+"


class RequestedService(str, Enum):
    AI_AUTOMATION = "ai_automation"
    CRM_AUTOMATION = "crm_automation"
    LLM_INTEGRATION = "llm_integration"
    KNOWLEDGE_ASSISTANT = "knowledge_assistant"
    AI_INFRASTRUCTURE = "ai_infrastructure"
    OTHER = "other"


class BudgetRange(str, Enum):
    UNDER_1000 = "under_1000"
    FROM_1000_TO_1999 = "1000_1999"
    FROM_2000_TO_4999 = "2000_4999"
    FROM_5000_TO_9999 = "5000_9999"
    FROM_10000 = "10000_plus"
    NOT_SURE = "not_sure"


class ProjectTimeline(str, Enum):
    IMMEDIATELY = "immediately"
    WITHIN_30_DAYS = "within_30_days"
    ONE_TO_THREE_MONTHS = "1_3_months"
    THREE_TO_SIX_MONTHS = "3_6_months"
    EXPLORING = "exploring"


class PreferredContactMethod(str, Enum):
    EMAIL = "email"
    PHONE = "phone"
    VIDEO_CALL = "video_call"


class QualificationStatus(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"
    DISQUALIFIED = "disqualified"


class LeadCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: str | None = Field(default=None, min_length=7, max_length=50)
    job_title: str | None = Field(default=None, max_length=150)
    company_name: str = Field(min_length=2, max_length=255)
    website: HttpUrl
    industry: str = Field(min_length=2, max_length=150)
    company_size: CompanySize
    requested_service: RequestedService
    problem_description: str = Field(min_length=30, max_length=3000)
    budget_range: BudgetRange
    project_timeline: ProjectTimeline
    preferred_contact_method: PreferredContactMethod
    consent_to_contact: bool

    @model_validator(mode="after")
    def validate_contact_preferences(self) -> "LeadCreate":
        if not self.consent_to_contact:
            raise ValueError("Consent to contact is required")

        if (
            self.preferred_contact_method == PreferredContactMethod.PHONE
            and not self.phone
        ):
            raise ValueError(
                "A phone number is required when phone is the preferred contact method"
            )

        return self


class LeadQualification(BaseModel):
    score: int = Field(ge=0, le=100)
    status: QualificationStatus
    summary: str
    positive_signals: list[str]
    risk_signals: list[str]
    recommended_action: str
    scoring_version: str


class LeadAccepted(BaseModel):
    id: UUID
    status: str
    message: str
    received_at: datetime
    qualification: LeadQualification | None = None

    @classmethod
    def from_submission(
        cls,
        qualification: LeadQualification | None = None,
    ) -> "LeadAccepted":
        return cls(
            id=uuid4(),
            status="submitted",
            message="Thank you. Your project details have been received for review.",
            received_at=datetime.now(timezone.utc),
            qualification=qualification,
        )