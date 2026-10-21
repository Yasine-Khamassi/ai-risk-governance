# The traceability thread

One technical weakness, followed all the way to a managed business risk. This is
the single strongest artefact in the portfolio: it connects a red-team finding to a
leadership-level decision with evidence at every step.

**Finding (Project 1).** The customer-support bot disclosed its system prompt under
a `system-prompt-extract` probe — OWASP LLM07. Ground truth: the system prompt
appeared verbatim in the model output.

**→ Risk (`risk-001`).** Logged against `sys-support-bot`: likelihood high, impact
high, treatment *mitigate*. A technical probe is now a line item leadership can own.

**→ Control (`ctl-output-filter`).** Output filtering that blocks secret and
system-prompt disclosure outside the model. Mapped to **NIST AI RMF MANAGE-2.2** and
OWASP LLM02/LLM07, MITRE ATLAS AML.T0057.

**→ Evidence (`ev-001`).** The control is tested by the Project 1 red-team runner in
both modes. Proof: **vulnerable 1/10 → defended 0/10**, last tested 2026-10-21.

**→ Retest & closure.** The defended run shows 0/10; `risk-001` moves to
*mitigated*. If the system prompt or guardrail changes, CI reruns the control tests
and the evidence is refreshed — the loop stays closed.

The same thread runs for the RAG cross-role leak (`risk-002` → `ctl-entitlement-filter`),
the agent excessive-agency finding (`risk-004` → `ctl-tool-gateway`) and the
monitoring gap (`risk-005` → `ctl-detections`). One risk remains deliberately
**open**: `risk-003`, the residual RAG injection that labelling alone does not fully
stop — tracked honestly rather than closed on paper.
