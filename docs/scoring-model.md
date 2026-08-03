# Lead Qualification Scoring Model

## Purpose

This document defines the deterministic scoring model used to evaluate and prioritize incoming leads.

The system generates a score between 0 and 100.

The rule-based score is authoritative. The LLM may explain the result, summarize the lead, identify risks, and recommend actions, but it cannot replace the final numerical score.

## Priority Levels

```text
80–100: High priority
55–79: Medium priority
0–54: Low priority
```

Certain disqualification rules may override the numerical score.

## Scoring Categories

| Criterion | Maximum Points |
|---|---:|
| Service fit | 25 |
| Budget fit | 20 |
| Project urgency | 15 |
| Decision authority | 15 |
| Company fit | 10 |
| Timeline clarity | 10 |
| Information completeness | 5 |
| **Total** | **100** |

## 1. Service Fit — 25 Points

| Requirement | Points |
|---|---:|
| Strong fit: AI automation, CRM workflow, RAG, LLM integration, OpenShift, Kubernetes, or AI infrastructure | 25 |
| Good fit: API integration, reporting automation, document processing, backend automation | 20 |
| Partial fit: General software project with an automation component | 12 |
| Weak fit: Unclear request or work outside the primary services | 5 |
| No fit: Job inquiry, unrelated training request, spam, or unrelated service | 0 |

Strong-fit examples:

- CRM lead automation
- Internal knowledge assistant
- AI customer-support triage
- Business-process automation
- LLM integration
- OpenShift AI deployment
- Kubernetes-based AI infrastructure

## 2. Budget Fit — 20 Points

Initial configurable budget bands:

| Budget | Points |
|---|---:|
| USD 10,000 or more | 20 |
| USD 5,000–9,999 | 17 |
| USD 2,000–4,999 | 13 |
| USD 1,000–1,999 | 7 |
| Below USD 1,000 | 2 |
| Not provided | 5 |

A missing budget should not automatically disqualify a lead.

## 3. Project Urgency — 15 Points

| Urgency | Points |
|---|---:|
| Critical business or operational problem | 15 |
| Active project with a clear deadline | 12 |
| Important project planned for the current quarter | 9 |
| Early research or exploration | 5 |
| No clear urgency | 0 |

Urgency should be based on the business situation, not emotional wording alone.

## 4. Decision Authority — 15 Points

| Role | Points |
|---|---:|
| Founder, owner, CEO, CTO, CIO, COO, or authorized executive | 15 |
| Director, department head, operations manager, or engineering manager | 12 |
| Project manager, technical lead, or strong internal champion | 9 |
| Individual contributor researching for a team | 5 |
| Student, job seeker, vendor, or unrelated contact | 0 |

Unclear authority should be flagged for human review.

## 5. Company Fit — 10 Points

| Company Profile | Points |
|---|---:|
| Established B2B company with clear automation potential | 10 |
| Technology company, agency, consultancy, or service provider | 9 |
| Growing small business with a defined workflow | 7 |
| Very early startup without process maturity | 4 |
| Individual or non-commercial inquiry | 1 |
| Spam or unrelated organization | 0 |

Company size is only one signal. A small company with a valuable operational problem may still be a strong lead.

## 6. Timeline Clarity — 10 Points

| Timeline | Points |
|---|---:|
| Clear start date and completion target | 10 |
| Expected to begin within 30 days | 8 |
| Expected to begin within 1–3 months | 6 |
| Future project without a committed date | 3 |
| No timeline information | 1 |

Unrealistically urgent deadlines should be flagged as delivery risks.

## 7. Information Completeness — 5 Points

| Submission Quality | Points |
|---|---:|
| Clear problem, process, outcome, budget, and timeline | 5 |
| Most important details provided | 4 |
| Basic need described but key details missing | 2 |
| Extremely vague submission | 0 |

## Final Score

```text
Final Score =
Service Fit
+ Budget Fit
+ Project Urgency
+ Decision Authority
+ Company Fit
+ Timeline Clarity
+ Information Completeness
```

The score must remain between 0 and 100.

## Example

A lead submits the following:

- Needs CRM lead-routing automation
- Budget is USD 4,000
- Wants to begin within 30 days
- Contact is an operations director
- Company is a 40-person B2B agency
- Business problem and desired outcome are clearly described

Possible score:

```text
Service fit:              25
Budget fit:               13
Project urgency:          12
Decision authority:       12
Company fit:              10
Timeline clarity:          8
Information completeness: 5
                          ---
Total score:              85
Priority: High
```

## Override Rules

### Automatic Low Priority

- Student project
- Job application
- Vendor solicitation
- Training-only inquiry
- No clear business problem
- No valid contact information

### Automatic Rejection

- Spam
- Fraud attempt
- Malicious content
- Illegal request
- Repeated abusive submission

### Mandatory Human Review

- Large budget with vague requirements
- Government or public-sector procurement
- Regulated industry
- Security-critical infrastructure
- Sensitive personal data
- Unrealistic deadline
- Conflicting qualification signals

## LLM Role

The LLM may generate:

- Business-problem summary
- Qualification explanation
- Risk flags
- Missing-information list
- Recommended next action
- Suggested response draft

Example structured output:

```json
{
  "summary": "The prospect wants to automate CRM lead intake and routing.",
  "service_fit": "strong",
  "risk_flags": [],
  "missing_information": [
    "Current CRM platform",
    "Monthly lead volume"
  ],
  "recommended_action": "Schedule a technical discovery call",
  "confidence": 0.91
}
```

The LLM does not generate the authoritative numerical score.

## Explainability

The reviewer interface should display:

```text
Final score: 85/100
Priority: High

Service fit: 25/25
Budget fit: 13/20
Urgency: 12/15
Decision authority: 12/15
Company fit: 10/10
Timeline clarity: 8/10
Information completeness: 5/5
```

## Configuration

Scoring weights and thresholds should eventually be stored in configuration.

Future configuration may support:

- Different industries
- Different service packages
- Regional pricing bands
- Enterprise and small-business profiles
- Customer-specific scoring rules

## Evaluation Metrics

The scoring model should later be evaluated using:

- High-priority lead conversion rate
- False-positive rate
- False-negative rate
- Reviewer score adjustments
- Lead response time
- Manual reassignment rate
- Qualified-to-discovery-call rate
