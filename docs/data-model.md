# Data Model

## Purpose

This document defines the initial PostgreSQL data model for the AI Lead Qualification and CRM Automation system.

The model supports:

- Lead storage
- Qualification results
- AI-generated drafts
- Human approval
- CRM synchronization
- Audit logging
- Workflow failure recovery

UUIDs should be used as primary keys.

All timestamps should use timezone-aware values.

## Core Relationships

```text
leads
 ├── qualification_results
 ├── email_drafts
 ├── approval_requests
 ├── crm_sync_events
 ├── audit_events
 └── workflow_failures
```

One lead may have multiple qualification results, drafts, approval requests, CRM attempts, audit events, and failures.

## `leads`

Stores the main lead record.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `full_name` | VARCHAR(150) | Contact name |
| `email` | VARCHAR(255) | Normalized work email |
| `phone` | VARCHAR(50), nullable | Contact phone |
| `job_title` | VARCHAR(150), nullable | Contact role |
| `company_name` | VARCHAR(255) | Company name |
| `company_domain` | VARCHAR(255), nullable | Normalized domain |
| `company_size` | VARCHAR(50), nullable | Company-size band |
| `industry` | VARCHAR(150), nullable | Industry |
| `country` | VARCHAR(100), nullable | Country |
| `requested_service` | VARCHAR(100) | Requested service |
| `problem_description` | TEXT | Business problem |
| `budget_range` | VARCHAR(50), nullable | Budget band |
| `project_timeline` | VARCHAR(50), nullable | Expected timeline |
| `current_tools` | TEXT, nullable | Existing systems |
| `source` | VARCHAR(50) | Website, API, webhook, or manual |
| `status` | VARCHAR(50) | Workflow status |
| `priority` | VARCHAR(20), nullable | High, medium, or low |
| `assigned_to` | UUID, nullable | Assigned reviewer |
| `crm_contact_id` | VARCHAR(255), nullable | CRM contact ID |
| `crm_company_id` | VARCHAR(255), nullable | CRM company ID |
| `crm_deal_id` | VARCHAR(255), nullable | CRM deal ID |
| `consent_to_contact` | BOOLEAN | Contact consent |
| `created_at` | TIMESTAMPTZ | Created timestamp |
| `updated_at` | TIMESTAMPTZ | Updated timestamp |
| `deleted_at` | TIMESTAMPTZ, nullable | Soft-delete timestamp |

Recommended indexes:

```text
email
company_domain
status
priority
created_at
crm_contact_id
```

## `qualification_results`

Stores each qualification calculation.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `lead_id` | UUID | Foreign key to leads |
| `version` | INTEGER | Scoring version |
| `service_fit_score` | INTEGER | 0–25 |
| `budget_fit_score` | INTEGER | 0–20 |
| `urgency_score` | INTEGER | 0–15 |
| `authority_score` | INTEGER | 0–15 |
| `company_fit_score` | INTEGER | 0–10 |
| `timeline_score` | INTEGER | 0–10 |
| `completeness_score` | INTEGER | 0–5 |
| `total_score` | INTEGER | 0–100 |
| `priority` | VARCHAR(20) | High, medium, or low |
| `rule_version` | VARCHAR(50) | Scoring rules version |
| `llm_summary` | TEXT, nullable | AI-generated summary |
| `llm_explanation` | TEXT, nullable | AI explanation |
| `llm_confidence` | DECIMAL(5,4), nullable | Confidence value |
| `risk_flags` | JSONB | Identified risks |
| `missing_information` | JSONB | Missing details |
| `recommended_action` | TEXT, nullable | Suggested action |
| `model_provider` | VARCHAR(100), nullable | AI provider |
| `model_name` | VARCHAR(100), nullable | Model name |
| `prompt_version` | VARCHAR(50), nullable | Prompt version |
| `created_at` | TIMESTAMPTZ | Created timestamp |

The category scores must stay within their defined ranges.

The total score must equal the sum of all category scores.

## `email_drafts`

Stores generated and manually edited responses.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `lead_id` | UUID | Foreign key |
| `qualification_result_id` | UUID, nullable | Related score |
| `version` | INTEGER | Draft version |
| `subject` | VARCHAR(255) | Email subject |
| `body_text` | TEXT | Plain-text body |
| `body_html` | TEXT, nullable | Sanitized HTML body |
| `generation_source` | VARCHAR(50) | LLM, template, or manual |
| `template_name` | VARCHAR(100), nullable | Template identifier |
| `model_name` | VARCHAR(100), nullable | Model used |
| `prompt_version` | VARCHAR(50), nullable | Prompt version |
| `created_by` | UUID, nullable | User or system actor |
| `is_final` | BOOLEAN | Approved version |
| `created_at` | TIMESTAMPTZ | Created timestamp |
| `updated_at` | TIMESTAMPTZ | Updated timestamp |

Draft history should be preserved.

## `approval_requests`

Stores human-review decisions.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `lead_id` | UUID | Foreign key |
| `email_draft_id` | UUID, nullable | Draft being reviewed |
| `qualification_result_id` | UUID | Score being reviewed |
| `status` | VARCHAR(30) | Pending, approved, rejected, or changes_requested |
| `requested_at` | TIMESTAMPTZ | Review request time |
| `reviewed_at` | TIMESTAMPTZ, nullable | Decision time |
| `requested_from` | UUID, nullable | Assigned reviewer |
| `reviewed_by` | UUID, nullable | Reviewer |
| `review_notes` | TEXT, nullable | Reviewer notes |
| `rejection_reason` | VARCHAR(100), nullable | Rejection category |
| `final_priority` | VARCHAR(20), nullable | Reviewer-confirmed priority |
| `created_at` | TIMESTAMPTZ | Created timestamp |
| `updated_at` | TIMESTAMPTZ | Updated timestamp |

Sending is not allowed without an approved request.

## `crm_sync_events`

Stores CRM synchronization attempts.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `lead_id` | UUID | Foreign key |
| `provider` | VARCHAR(50) | CRM provider |
| `operation` | VARCHAR(50) | Search, create, update, add note, or create task |
| `status` | VARCHAR(30) | Pending, success, failed, or retrying |
| `external_object_type` | VARCHAR(50) | Contact, company, deal, or task |
| `external_object_id` | VARCHAR(255), nullable | CRM object ID |
| `request_payload` | JSONB, nullable | Sanitized request data |
| `response_payload` | JSONB, nullable | Sanitized response data |
| `error_code` | VARCHAR(100), nullable | Error code |
| `error_message` | TEXT, nullable | Sanitized error |
| `attempt_number` | INTEGER | Retry attempt |
| `idempotency_key` | VARCHAR(255) | Duplicate-operation protection |
| `started_at` | TIMESTAMPTZ | Start time |
| `completed_at` | TIMESTAMPTZ, nullable | Completion time |
| `next_retry_at` | TIMESTAMPTZ, nullable | Next retry |
| `created_at` | TIMESTAMPTZ | Created timestamp |

Authentication tokens must never be stored in request or response payloads.

## `audit_events`

Stores immutable records of important actions.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `lead_id` | UUID, nullable | Related lead |
| `actor_type` | VARCHAR(30) | User, system, workflow, or integration |
| `actor_id` | UUID, nullable | Actor identity |
| `event_type` | VARCHAR(100) | Structured event name |
| `previous_state` | VARCHAR(50), nullable | Previous status |
| `new_state` | VARCHAR(50), nullable | New status |
| `correlation_id` | UUID | Workflow correlation ID |
| `ip_address` | INET, nullable | Request origin |
| `user_agent` | TEXT, nullable | Client metadata |
| `metadata` | JSONB | Sanitized event information |
| `created_at` | TIMESTAMPTZ | Immutable timestamp |

Audit events must not contain passwords, tokens, API keys, or unnecessary personal information.

## `workflow_failures`

Stores workflow failures.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `lead_id` | UUID, nullable | Related lead |
| `workflow_name` | VARCHAR(100) | Workflow identifier |
| `workflow_execution_id` | VARCHAR(255), nullable | n8n execution ID |
| `step_name` | VARCHAR(100) | Failed step |
| `error_type` | VARCHAR(100) | Error category |
| `error_message` | TEXT | Sanitized description |
| `is_retryable` | BOOLEAN | Retry eligibility |
| `attempt_number` | INTEGER | Current attempt |
| `max_attempts` | INTEGER | Retry limit |
| `next_retry_at` | TIMESTAMPTZ, nullable | Scheduled retry |
| `resolved_at` | TIMESTAMPTZ, nullable | Resolution time |
| `resolved_by` | UUID, nullable | Resolver |
| `resolution_notes` | TEXT, nullable | Resolution details |
| `created_at` | TIMESTAMPTZ | Failure timestamp |

## Future Tables

Possible future tables:

```text
users
roles
user_roles
organizations
scoring_configurations
prompt_templates
email_delivery_events
follow_up_tasks
webhook_events
lead_attachments
```

## Personally Identifiable Information

Sensitive data includes:

- Name
- Email
- Phone
- Job title
- Company information
- Message content
- IP address
- Email communication

Controls should include:

- Restricted access
- Encryption in transit
- Encryption at rest where available
- Data-retention rules
- Log masking
- Access logging
- Secure deletion

## Initial Retention Policy

```text
Invalid leads: 90 days
Rejected leads: 90 days
Qualified leads: 24 months
Audit events: 24 months
Workflow failures: 180 days
Integration payloads: 30–90 days
```

These values should remain configurable.

## Migration Strategy

Database schema changes should use:

```text
Alembic with SQLAlchemy
```

Every schema change should include:

- Forward migration
- Rollback strategy
- Compatibility review
- Migration test
- Production-impact note
