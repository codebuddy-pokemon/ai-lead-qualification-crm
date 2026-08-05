"use client";

import { FormEvent, useState } from "react";

type QualificationStatus = "hot" | "warm" | "cold" | "disqualified";

type Qualification = {
  score: number;
  status: QualificationStatus;
  summary: string;
  positive_signals: string[];
  risk_signals: string[];
  recommended_action: string;
  scoring_version: string;
};

type SubmissionState =
  | { kind: "idle" }
  | { kind: "submitting" }
  | {
      kind: "success";
      message: string;
      id: string;
      qualification: Qualification;
    }
  | { kind: "error"; message: string };

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

function errorMessage(payload: unknown): string {
  if (typeof payload === "object" && payload !== null && "detail" in payload) {
    const detail = (payload as { detail: unknown }).detail;
    if (typeof detail === "string") return detail;
  }
  return "We couldn’t submit your details. Please review the form and try again.";
}

export function LeadIntakeForm() {
  const [submission, setSubmission] = useState<SubmissionState>({ kind: "idle" });
  const [preferredContact, setPreferredContact] = useState("email");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmission({ kind: "submitting" });

    const form = event.currentTarget;
    const formData = new FormData(form);
    const phone = String(formData.get("phone") ?? "").trim();

    const payload = {
      full_name: formData.get("full_name"),
      email: formData.get("email"),
      phone: phone || null,
      job_title: String(formData.get("job_title") ?? "").trim() || null,
      company_name: formData.get("company_name"),
      website: formData.get("website"),
      industry: formData.get("industry"),
      company_size: formData.get("company_size"),
      requested_service: formData.get("requested_service"),
      problem_description: formData.get("problem_description"),
      budget_range: formData.get("budget_range"),
      project_timeline: formData.get("project_timeline"),
      preferred_contact_method: formData.get("preferred_contact_method"),
      consent_to_contact: formData.get("consent_to_contact") === "on",
    };

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/leads`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const result: unknown = await response.json();

      if (!response.ok) {
        throw new Error(errorMessage(result));
      }

      const accepted = result as {
  id: string;
  message: string;
  qualification: Qualification | null;
};

if (!accepted.qualification) {
  throw new Error("The lead was submitted, but no qualification result was returned.");
}

setSubmission({
  kind: "success",
  message: accepted.message,
  id: accepted.id,
  qualification: accepted.qualification,
});
      form.reset();
      setPreferredContact("email");
    } catch (error) {
      setSubmission({
        kind: "error",
        message: error instanceof Error ? error.message : "Unexpected submission error.",
      });
    }
  }

  if (submission.kind === "success") {
  const qualification = submission.qualification;

  return (
    <div className="success-card" role="status">
      <span className="success-card__icon" aria-hidden="true">
        ✓
      </span>

      <p className="eyebrow">Portfolio demonstration</p>
      <h3>Lead qualification completed</h3>
      <p>{submission.message}</p>

      <div className="qualification-result">
        <div>
          <strong>Lead score</strong>
          <p>{qualification.score}/100</p>
        </div>

        <div>
          <strong>Qualification</strong>
          <p>{qualification.status.toUpperCase()}</p>
        </div>
      </div>

      <div className="qualification-section">
        <h4>Assessment summary</h4>
        <p>{qualification.summary}</p>
      </div>

      <div className="qualification-section">
        <h4>Positive signals</h4>
        {qualification.positive_signals.length > 0 ? (
          <ul>
            {qualification.positive_signals.map((signal) => (
              <li key={signal}>{signal}</li>
            ))}
          </ul>
        ) : (
          <p>No strong positive signals were identified.</p>
        )}
      </div>

      <div className="qualification-section">
        <h4>Risk signals</h4>
        {qualification.risk_signals.length > 0 ? (
          <ul>
            {qualification.risk_signals.map((signal) => (
              <li key={signal}>{signal}</li>
            ))}
          </ul>
        ) : (
          <p>No significant risk signals were identified.</p>
        )}
      </div>

      <div className="qualification-section">
        <h4>Recommended sales action</h4>
        <p>{qualification.recommended_action}</p>
      </div>

      <p className="reference">
        Reference: {submission.id.slice(0, 8).toUpperCase()}
      </p>

      <button
        className="button button--secondary"
        onClick={() => setSubmission({ kind: "idle" })}
      >
        Submit another project
      </button>
    </div>
  );
}

  return (
    <form className="lead-form" onSubmit={handleSubmit}>
      <fieldset>
        <legend>Contact details</legend>
        <div className="field-grid">
          <label>
            <span>Full name *</span>
            <input name="full_name" autoComplete="name" minLength={2} maxLength={150} required />
          </label>
          <label>
            <span>Business email *</span>
            <input name="email" type="email" autoComplete="email" maxLength={255} required />
          </label>
          <label>
            <span>Job title</span>
            <input name="job_title" autoComplete="organization-title" maxLength={150} />
          </label>
          <label>
            <span>Phone {preferredContact === "phone" ? "*" : "(optional)"}</span>
            <input
              name="phone"
              type="tel"
              autoComplete="tel"
              minLength={7}
              maxLength={50}
              required={preferredContact === "phone"}
            />
          </label>
        </div>
      </fieldset>

      <fieldset>
        <legend>Company</legend>
        <div className="field-grid">
          <label>
            <span>Company name *</span>
            <input name="company_name" autoComplete="organization" minLength={2} maxLength={255} required />
          </label>
          <label>
            <span>Website *</span>
            <input name="website" type="url" placeholder="https://" autoComplete="url" required />
          </label>
          <label>
            <span>Industry *</span>
            <input name="industry" maxLength={150} placeholder="e.g. B2B marketing" required />
          </label>
          <label>
            <span>Company size *</span>
            <select name="company_size" defaultValue="" required>
              <option value="" disabled>Select team size</option>
              <option value="1">Just me</option>
              <option value="2-10">2–10 people</option>
              <option value="11-50">11–50 people</option>
              <option value="51-200">51–200 people</option>
              <option value="201-1000">201–1,000 people</option>
              <option value="1000+">More than 1,000</option>
            </select>
          </label>
        </div>
      </fieldset>

      <fieldset>
        <legend>Project</legend>
        <div className="field-grid">
          <label className="field-grid__wide">
            <span>Area of interest *</span>
            <select name="requested_service" defaultValue="" required>
              <option value="" disabled>Select the closest match</option>
              <option value="ai_automation">AI workflow automation</option>
              <option value="crm_automation">CRM and sales automation</option>
              <option value="llm_integration">LLM or API integration</option>
              <option value="knowledge_assistant">Internal knowledge assistant</option>
              <option value="ai_infrastructure">AI infrastructure or OpenShift</option>
              <option value="other">Another workflow challenge</option>
            </select>
          </label>
          <label className="field-grid__wide">
            <span>What is happening today, and what should improve? *</span>
            <textarea
              name="problem_description"
              rows={6}
              minLength={30}
              maxLength={3000}
              placeholder="Describe the manual steps, delays, or errors—and the outcome you want."
              required
            />
            <small>Include enough context for a useful first review (minimum 30 characters).</small>
          </label>
          <label>
            <span>Estimated budget *</span>
            <select name="budget_range" defaultValue="" required>
              <option value="" disabled>Select a range</option>
              <option value="under_1000">Under $1,000</option>
              <option value="1000_1999">$1,000–$1,999</option>
              <option value="2000_4999">$2,000–$4,999</option>
              <option value="5000_9999">$5,000–$9,999</option>
              <option value="10000_plus">$10,000+</option>
              <option value="not_sure">Not sure yet</option>
            </select>
          </label>
          <label>
            <span>Preferred timeline *</span>
            <select name="project_timeline" defaultValue="" required>
              <option value="" disabled>Select a timeline</option>
              <option value="immediately">As soon as possible</option>
              <option value="within_30_days">Within 30 days</option>
              <option value="1_3_months">Within 1–3 months</option>
              <option value="3_6_months">Within 3–6 months</option>
              <option value="exploring">Researching options</option>
            </select>
          </label>
          <label className="field-grid__wide">
            <span>Preferred contact method *</span>
            <select
              name="preferred_contact_method"
              value={preferredContact}
              onChange={(event) => setPreferredContact(event.target.value)}
              required
            >
              <option value="email">Email</option>
              <option value="video_call">Video call</option>
              <option value="phone">Phone</option>
            </select>
          </label>
        </div>
      </fieldset>

      <label className="consent">
        <input name="consent_to_contact" type="checkbox" required />
        <span>I agree to be contacted about this project. My details will only be used to review and respond to this inquiry. *</span>
      </label>

      {submission.kind === "error" && <p className="form-error" role="alert">{submission.message}</p>}

      <button className="button" type="submit" disabled={submission.kind === "submitting"}>
        {submission.kind === "submitting" ? "Submitting…" : "Request assessment"}
        <span aria-hidden="true">→</span>
      </button>
    </form>
  );
}

