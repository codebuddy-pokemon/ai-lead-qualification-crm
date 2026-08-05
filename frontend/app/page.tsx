import { LeadIntakeForm } from "../components/lead-intake-form";

export default function Home() {
  return (
    <main>
      <section className="hero" aria-labelledby="page-title">
        <div className="hero__content">
          <a className="brand" href="#page-title" aria-label="FlowSignal home">
            <span className="brand__mark">F</span>
            <span>FlowSignal</span>
          </a>

          <div className="hero__copy">
            <p className="eyebrow">AI workflow assessment</p>
            <h1 id="page-title">Turn a costly manual process into a clear automation plan.</h1>
            <p className="hero__lede">
              Tell us where work is slowing down. We’ll review the opportunity, identify the
              strongest automation path, and recommend a practical next step.
            </p>
          </div>

          <ul className="benefits" aria-label="Assessment benefits">
            <li><span>01</span> A focused review of your current workflow</li>
            <li><span>02</span> Transparent fit and priority assessment</li>
            <li><span>03</span> Human review before any follow-up</li>
          </ul>
        </div>
      </section>

      <section className="form-panel" aria-label="Project intake">
        <div className="form-panel__inner">
          <div className="form-heading">
            <p className="eyebrow">Start the conversation</p>
            <h2>What would you like to improve?</h2>
            <p>Fields marked with * are required. Most people finish in about three minutes.</p>
          </div>
          <LeadIntakeForm />
        </div>
      </section>
    </main>
  );
}

