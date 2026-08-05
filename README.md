# AI Lead Qualification & CRM Automation

> Portfolio demonstration currently under development.

An AI-powered workflow that captures incoming leads, evaluates their business fit, assigns a transparent qualification score, drafts a personalized response, and updates the CRM while keeping a human approval step before external communication.

## Business Problem

Companies receive leads through website forms, email, referrals, advertisements, and other channels.

Sales teams often need to manually:

- Extract contact and company information
- Research the prospect
- Determine whether the lead is relevant
- Enter information into the CRM
- Decide which salesperson should handle it
- Prepare an initial response
- Remember when to follow up

This creates slow response times, inconsistent qualification, incomplete CRM data, and lost sales opportunities.

## Proposed Workflow

```text
Lead received
      ↓
Contact and company data extracted
      ↓
Lead information validated and enriched
      ↓
AI evaluates business fit and purchase intent
      ↓
Qualification score and reasoning generated
      ↓
CRM record created or updated
      ↓
Personalized response drafted
      ↓
Human reviews and approves the response
      ↓
Sales representative notified
      ↓
Follow-up task scheduled
```

## MVP Features

- Website lead-capture form
- Structured lead database
- AI lead classification
- Qualification score from 0–100
- Explanation behind the score
- High-, medium-, and low-priority routing
- Personalized email draft
- CRM record creation or update
- Sales-team notification
- Human approval before sending
- Workflow event and activity log
- Basic lead dashboard

## Initial Qualification Criteria

The system will evaluate factors such as:

- Company size
- Industry
- Geographic location
- Requested service
- Budget range
- Project timeline
- Decision-making authority
- Problem urgency
- Fit with available services
- Completeness of submitted information

The scoring criteria will remain configurable rather than being permanently embedded in the AI prompt.

## Planned Architecture

```text
Lead Form
   ↓
Backend API
   ↓
Validation and Enrichment
   ↓
Qualification Engine
   ↓
PostgreSQL Database
   ↓
CRM Integration
   ↓
Approval Dashboard
   ↓
Email and Sales Notification
```

## Proposed Technology Stack

- Frontend: Next.js
- Backend: FastAPI
- Database: PostgreSQL
- Automation: n8n
- CRM: HubSpot test account or local CRM adapter
- AI: OpenAI-compatible API
- Deployment: Docker Compose initially
- Infrastructure: Kubernetes/OpenShift after MVP

Detailed implementation decisions, integration patterns, and architectural trade-offs will be documented as the system is developed.

## Safety and Reliability

This project will include:

- Human approval before external messages are sent
- Structured AI outputs
- Input validation
- Configurable qualification rules
- Audit logs
- Error handling and retry logic
- Environment-based secrets management
- Protection against prompt injection from lead-submitted content
- Fallback behavior when the AI service is unavailable

## Expected Business Value

The workflow is intended to help businesses:

- Respond to qualified leads faster
- Reduce repetitive sales administration
- Improve CRM data quality
- Apply consistent qualification criteria
- Prioritize high-value opportunities
- Maintain oversight over AI-generated communication

## Project Roadmap

### Phase 1 — Discovery and Design

- Define the target business
- Map the manual sales process
- Finalize scoring criteria
- Design workflow and architecture

### Phase 2 — Core MVP

- Build the lead form
- Store lead information
- Implement qualification logic
- Display score and reasoning
- Generate email drafts

### Phase 3 — Automation

- Add n8n workflow
- Add CRM integration
- Add notifications
- Add approval process
- Add activity logs

### Phase 4 — Production Readiness

- Containerize the application
- Add authentication
- Add monitoring and error handling
- Add automated tests
- Prepare Kubernetes/OpenShift deployment

## Repository Structure

```text
ai-lead-qualification-crm/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── services/
│   │   ├── main.py
│   │   └── routes.py
│   ├── tests/
│   ├── requirements.txt
│   └── requirements-dev.txt
├── frontend/
│   ├── app/
│   ├── components/
│   └── package.json
├── docs/
│   ├── architecture.md
│   ├── data-model.md
│   ├── scoring-model.md
│   ├── security.md
│   └── workflow.md
├── .env.example
└── README.md
```

## Project Status

**Current stage:** Validated lead-intake vertical slice

The current implementation includes:

- A responsive Next.js project-intake form
- Required-field and browser-level validation
- A versioned FastAPI lead-submission endpoint
- Backend validation for email, URL, consent, field lengths, and contact preferences
- A health endpoint and automated API tests
- A human-review confirmation state after submission

Lead submissions are held in a temporary in-memory store during this first slice. PostgreSQL persistence, deterministic scoring, AI analysis, CRM synchronization, notifications, and outbound communication remain intentionally outside this increment.

## Local Development

### 1. Start the API

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

### 2. Start the frontend

In a second terminal:

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000` and submit a sample lead.

### 3. Run verification

```bash
cd backend
.venv/bin/python -m pytest -q
```

```bash
cd frontend
npm run lint
npm run build
```

This is an original portfolio project designed to demonstrate AI workflow automation, CRM integration, human-in-the-loop controls, and production deployment practices.
