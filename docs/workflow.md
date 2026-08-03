# Lead Qualification Workflow

## Purpose

This document defines the full lead lifecycle from submission to qualification, human approval, CRM synchronization, response delivery, and follow-up.

The workflow follows three principles:

1. AI supports decisions but does not take uncontrolled external actions.
2. Human approval is required before sending customer communication.
3. Every important action is logged for auditability and recovery.

## Workflow Overview

```text
Lead submitted
      ↓
Input validated
      ↓
Duplicate check performed
      ↓
Lead stored in PostgreSQL
      ↓
Rule-based qualification score calculated
      ↓
LLM generates summary and explanation
      ↓
Response draft generated
      ↓
Human approval requested
      ↓
CRM record created or updated
      ↓
Approved response sent
      ↓
Follow-up task scheduled
      ↓
Workflow completed
```

## Lead Status Lifecycle

```text
submitted
→ validating
→ qualification_pending
→ qualified
→ awaiting_approval
→ approved
→ crm_sync_pending
→ synced_to_crm
→ response_pending
→ response_sent
→ follow_up_scheduled
→ completed
```

Alternative statuses:

```text
invalid
duplicate
rejected
failed
archived
```

## Status Definitions

### `submitted`

The lead has been received through the website form or API.

Actions:

- Generate a unique lead ID.
- Record the submission timestamp.
- Create an audit event.
- Assign a workflow correlation ID.

### `validating`

FastAPI validates:

- Required fields
- Email format
- Field lengths
- Supported service values
- Budget and timeline values
- Malicious or malformed input
- Consent fields where required

### `invalid`

The submission failed validation.

Examples:

- Invalid email
- Missing required fields
- Unsupported service category
- Excessively long input
- Malformed request body

Invalid leads are not sent to the LLM.

### `duplicate`

The system detects an existing lead using:

- Normalized email address
- Company domain
- Phone number
- Similar recent submission

Duplicate submissions should be linked to the existing lead instead of silently discarded.

### `qualification_pending`

The lead has passed validation and is ready for scoring.

### `qualified`

The system has completed:

- Deterministic scoring
- Priority classification
- LLM-generated summary
- Risk identification
- Missing-information analysis
- Recommended next action

### `awaiting_approval`

A reviewer can:

- Approve the recommendation
- Edit and approve the response
- Change the priority
- Reject the lead
- Request more information
- Regenerate the draft
- Reassign the lead
- Mark the submission as spam

### `approved`

The reviewer approved the final response and next action.

The approval record must include:

- Reviewer identity
- Approval timestamp
- Final response version
- Reviewer notes
- Any manual changes

### `rejected`

The reviewer decided not to proceed.

Possible rejection reasons:

- Outside service scope
- Budget mismatch
- Spam
- Student inquiry
- Job application
- Unsupported geography
- Insufficient information
- Vendor solicitation
- Other

### `crm_sync_pending`

The approved lead is waiting to be synchronized with the CRM.

### `synced_to_crm`

The CRM operation completed successfully.

The system stores:

- CRM provider
- External contact ID
- External company ID
- External deal ID
- Synchronization timestamp
- Operation result

### `response_pending`

The approved response is ready but has not yet been sent.

### `response_sent`

The system records:

- Recipient
- Message ID
- Sending account
- Delivery timestamp
- Approved response version
- Provider response

### `follow_up_scheduled`

A follow-up task is created in:

- The CRM
- The local application
- n8n
- A future calendar or task integration

### `completed`

The initial qualification workflow completed successfully.

### `failed`

An unrecoverable error occurred.

Examples:

- Database failure
- CRM authentication failure
- Email provider failure
- Workflow timeout
- Invalid integration response

The lead must remain visible and recoverable.

## Lead Submission Fields

Required fields:

- Full name
- Work email
- Company name
- Requested service
- Problem description
- Budget range
- Project timeline

Optional fields:

- Phone number
- Job title
- Company size
- Industry
- Country
- Current tools
- Preferred contact method

## Qualification Process

Qualification has two layers.

### Deterministic Scoring

The backend calculates the authoritative score using explicit rules.

### LLM Analysis

The LLM provides:

- Problem summary
- Qualification explanation
- Risk flags
- Missing information
- Recommended next action
- Suggested response approach

The LLM cannot directly overwrite the deterministic score.

## Human Approval

Before sending any external message, the backend verifies:

- The lead is approved.
- An approval record exists.
- The reviewer is authorized.
- A final draft is selected.
- The recipient email is valid.
- The response has not already been sent.

## CRM Integration

The CRM adapter should support:

```text
find_contact()
create_contact()
update_contact()
find_company()
create_company()
create_or_update_deal()
add_note()
create_follow_up_task()
```

The local PostgreSQL database remains the source of truth for workflow status.

## Failure Handling

### LLM Failure

- Keep the deterministic score.
- Mark AI explanation as unavailable.
- Route the lead to human review.
- Do not block lead storage.
- Do not send automatically.

### CRM Failure

- Keep the lead locally.
- Record the failed attempt.
- Retry with exponential backoff.
- Notify an administrator after repeated failures.
- Allow manual retry.

### Email Failure

- Preserve the approved draft.
- Do not mark the message as sent.
- Retry only when safe.
- Prevent duplicate delivery.
- Notify the reviewer when manual action is required.

### n8n Failure

- Preserve the original event.
- Store the workflow execution ID.
- Record the failed step.
- Allow replay from the last safe point.

## Retry Policy

```text
Attempt 1: Immediately
Attempt 2: After 1 minute
Attempt 3: After 5 minutes
Attempt 4: After 15 minutes
Attempt 5: After 1 hour
```

Non-retryable errors include:

- Invalid credentials
- Invalid recipient address
- Permission denied
- Invalid webhook signature
- Unsupported CRM field

## Idempotency

Idempotency protection must be used for:

- Lead submission
- CRM synchronization
- Email delivery
- n8n webhook execution
- Follow-up task creation

## Audit Events

```text
lead.submitted
lead.validated
lead.validation_failed
lead.duplicate_detected
qualification.completed
qualification.failed
draft.generated
draft.edited
approval.requested
approval.approved
approval.rejected
crm.sync_started
crm.sync_completed
crm.sync_failed
email.send_started
email.sent
email.failed
follow_up.created
workflow.completed
workflow.failed
```

Each audit event should contain:

- Event type
- Actor
- Lead ID
- Timestamp
- Previous state
- New state
- Correlation ID
- Sanitized metadata

## MVP Boundaries

The MVP will not include:

- Fully autonomous email sending
- Automatic pricing commitments
- Paid enrichment providers
- Multiple CRM platforms
- Social-media outreach
- Voice calling
- Contract generation
- Complex sales forecasting
