# Northwind AI Security & Governance

- AI systems: 4  |  tracked risks: 5  |  open: 1

## Risk register

| ID | System | Risk | OWASP | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| risk-001 | sys-support-bot | System-prompt / secret disclosure via prompt injection | LLM07 System Prompt Leakage | mitigated | Project 1 defended run: 0/10 |
| risk-002 | sys-rag-assistant | Cross-role retrieval of confidential HR documents | LLM02 Sensitive Information Disclosure | mitigated | Project 2 defended run: cross-role 0/2 |
| risk-003 | sys-rag-assistant | Indirect prompt injection via poisoned uploaded document | LLM01 Prompt Injection | open | Project 2 defended run: 1/2 injection still succeeded |
| risk-004 | sys-it-agent | Agent coerced into an unauthorized restricted-asset action | LLM06 Excessive Agency | mitigated | Project 3 defended run: 0/2 executed |
| risk-005 | sys-support-bot | Undetected misuse (no monitoring on AI traffic) | LLM-ops | mitigated | Project 4: 5/5 attack sessions detected, 0 false positives |

## Open actions

- risk-003: Indirect prompt injection via poisoned uploaded document (control ctl-data-separation)
