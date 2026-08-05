from app.models.lead import (
    BudgetRange,
    CompanySize,
    LeadCreate,
    LeadQualification,
    ProjectTimeline,
    QualificationStatus,
    RequestedService,
)


BUDGET_SCORES: dict[BudgetRange, int] = {
    BudgetRange.UNDER_1000: 2,
    BudgetRange.FROM_1000_TO_1999: 12,
    BudgetRange.FROM_2000_TO_4999: 20,
    BudgetRange.FROM_5000_TO_9999: 23,
    BudgetRange.FROM_10000: 25,
    BudgetRange.NOT_SURE: 5,
}

TIMELINE_SCORES: dict[ProjectTimeline, int] = {
    ProjectTimeline.IMMEDIATELY: 20,
    ProjectTimeline.WITHIN_30_DAYS: 18,
    ProjectTimeline.ONE_TO_THREE_MONTHS: 10,
    ProjectTimeline.THREE_TO_SIX_MONTHS: 8,
    ProjectTimeline.EXPLORING: 4,
}

COMPANY_SIZE_SCORES: dict[CompanySize, int] = {
    CompanySize.SOLO: 4,
    CompanySize.SMALL: 10,
    CompanySize.GROWING: 15,
    CompanySize.MID_MARKET: 15,
    CompanySize.LARGE: 12,
    CompanySize.ENTERPRISE: 10,
}

SERVICE_SCORES: dict[RequestedService, int] = {
    RequestedService.AI_AUTOMATION: 10,
    RequestedService.CRM_AUTOMATION: 10,
    RequestedService.LLM_INTEGRATION: 10,
    RequestedService.KNOWLEDGE_ASSISTANT: 10,
    RequestedService.AI_INFRASTRUCTURE: 10,
    RequestedService.OTHER: 5,
}

SERVICE_LABELS: dict[RequestedService, str] = {
    RequestedService.AI_AUTOMATION: "AI workflow automation",
    RequestedService.CRM_AUTOMATION: "CRM and sales automation",
    RequestedService.LLM_INTEGRATION: "LLM or API integration",
    RequestedService.KNOWLEDGE_ASSISTANT: "an internal knowledge assistant",
    RequestedService.AI_INFRASTRUCTURE: "AI infrastructure or OpenShift",
    RequestedService.OTHER: "another workflow improvement",
}


PAIN_KEYWORDS = {
    "manual",
    "delay",
    "delays",
    "error",
    "errors",
    "slow",
    "cost",
    "costly",
    "time",
    "hours",
    "repetitive",
    "duplicate",
    "missed",
    "inefficient",
    "bottleneck",
    "spreadsheet",
    "security",
    "secure",
    "governance",
    "compliance",
    "monitoring",
    "reliability",
    "reliable",
    "scaling",
    "scalable",
    "deployment",
    "automation",
    "downtime",
    "availability",
    "production",
    "integration",
}

DECISION_ROLE_KEYWORDS = {
    "owner",
    "founder",
    "co-founder",
    "ceo",
    "cto",
    "cio",
    "director",
    "head",
    "vp",
    "vice president",
    "manager",
    "partner",
}


def _problem_score(description: str) -> tuple[int, list[str], list[str]]:
    """Score problem clarity using only information supplied by the lead."""

    normalized = description.lower()
    matching_keywords = sorted(
        keyword for keyword in PAIN_KEYWORDS if keyword in normalized
    )

    score = 10
    positive_signals: list[str] = []
    risk_signals: list[str] = []

    if len(description) >= 100:
        score += 5
        positive_signals.append("The operational problem is described in useful detail")
    else:
        risk_signals.append("The problem description contains limited detail")

    if matching_keywords:
        score += 5
        positive_signals.append("The inquiry identifies a concrete operational pain")
    else:
        risk_signals.append("No specific cost, delay, error, or bottleneck was identified")

    return score, positive_signals, risk_signals


def _role_score(job_title: str | None) -> tuple[int, list[str], list[str]]:
    """Estimate contact-role fit without claiming decision authority."""

    if not job_title:
        return (
            2,
            [],
            ["The contact's role and purchasing involvement are not provided"],
        )

    normalized_title = job_title.lower()

    if any(keyword in normalized_title for keyword in DECISION_ROLE_KEYWORDS):
        return (
            10,
            ["The contact title suggests meaningful project involvement"],
            [],
        )

    return (
        6,
        ["A professional role was provided"],
        ["Decision-making authority is not confirmed"],
    )


def _status_from_score(score: int) -> QualificationStatus:
    if score >= 85:
        return QualificationStatus.HOT
    if score >= 60:
        return QualificationStatus.WARM
    if score >= 40:
        return QualificationStatus.COLD
    return QualificationStatus.DISQUALIFIED


def _recommended_action(status: QualificationStatus) -> str:
    actions = {
        QualificationStatus.HOT: (
            "Contact the lead within one business day and propose a discovery call."
        ),
        QualificationStatus.WARM: (
            "Send a personalized response and request any missing qualification details."
        ),
        QualificationStatus.COLD: (
            "Place the lead into a nurture sequence and review again if urgency increases."
        ),
        QualificationStatus.DISQUALIFIED: (
            "Send a courteous response and do not prioritize manual sales follow-up."
        ),
    }
    return actions[status]


def qualify_lead(lead: LeadCreate) -> LeadQualification:
    """Return a transparent, deterministic qualification assessment."""

    positive_signals: list[str] = []
    risk_signals: list[str] = []

    budget_score = BUDGET_SCORES[lead.budget_range]
    timeline_score = TIMELINE_SCORES[lead.project_timeline]
    company_score = COMPANY_SIZE_SCORES[lead.company_size]
    service_score = SERVICE_SCORES[lead.requested_service]

    problem_score, problem_positive, problem_risks = _problem_score(
        lead.problem_description
    )
    role_score, role_positive, role_risks = _role_score(lead.job_title)

    positive_signals.extend(problem_positive)
    positive_signals.extend(role_positive)
    risk_signals.extend(problem_risks)
    risk_signals.extend(role_risks)


    if budget_score >= 20:
        positive_signals.append("The stated budget fits a meaningful implementation")
    elif lead.budget_range == BudgetRange.UNDER_1000:
        risk_signals.append(
        "The stated budget is below the typical range for a full implementation"
    )
    elif budget_score <= 8:
        risk_signals.append(
        "The stated budget may not support a full implementation"
    )    

    if timeline_score >= 18:
        positive_signals.append("The project has strong near-term urgency")
    elif timeline_score <= 4:
        risk_signals.append("The lead is currently researching rather than buying")

    if company_score >= 15:
        positive_signals.append(
            "The company size fits the target customer profile"
        )

    score = (
        budget_score
        + timeline_score
        + company_score
        + service_score
        + problem_score
        + role_score
    )

    if (
        lead.budget_range == BudgetRange.UNDER_1000
        and role_score < 10
    ):
        score -= 5

    score = max(0, min(score, 100))

    status = _status_from_score(score)

    service_label = SERVICE_LABELS[lead.requested_service]
    company_name = lead.company_name.strip()

    summary = (
        f"{company_name} is seeking {service_label}. "
        f"The inquiry scored {score}/100 based on budget, urgency, company fit, "
        "problem clarity, service fit, and contact-role information."
    )


    return LeadQualification(
        score=score,
        status=status,
        summary=summary,
        positive_signals=positive_signals,
        risk_signals=risk_signals,
        recommended_action=_recommended_action(status),
        scoring_version="rules-v1",
    )
