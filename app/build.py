"""
Assemble the AI governance artefacts into an executive report and dashboard.

Loads the inventory, risk register, control mapping and evidence register,
validates that every link resolves (the traceability thread), and writes:
  - GOVERNANCE.md     : a readable report
  - dashboard.html    : a self-contained executive dashboard

    python -m app.build
"""

from __future__ import annotations

import json
import os

DATA = "data"


def _load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def validate(inv, risks, controls, evidence) -> list[str]:
    errors = []
    sys_ids = {s["id"] for s in inv}
    ctl_ids = {c["id"] for c in controls}
    ev_ids = {e["id"] for e in evidence}
    for r in risks:
        if r["system"] not in sys_ids:
            errors.append(f"{r['id']}: unknown system {r['system']}")
        if r["control"] not in ctl_ids:
            errors.append(f"{r['id']}: unknown control {r['control']}")
    for c in controls:
        if c["evidence"] not in ev_ids:
            errors.append(f"{c['id']}: unknown evidence {c['evidence']}")
    valid_tiers = {"low", "medium", "high", "critical"}
    for s in inv:
        if s["risk_tier"] not in valid_tiers:
            errors.append(f"{s['id']}: bad risk_tier {s['risk_tier']}")
    return errors


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_dashboard(inv, risks, controls, evidence) -> str:
    ctl_by = {c["id"]: c for c in controls}
    ev_by = {e["id"]: e for e in evidence}
    open_risks = [r for r in risks if r["status"] == "open"]
    tiers = {t: sum(1 for s in inv if s["risk_tier"] == t) for t in ("critical", "high", "medium", "low")}

    risk_rows = "".join(
        f"<tr><td><code>{_esc(r['id'])}</code></td><td>{_esc(r['title'])}</td>"
        f"<td>{_esc(r['owasp'])}</td><td>{_esc(r['impact'])}</td>"
        f"<td class='{'bad' if r['status']=='open' else 'ok'}'>{_esc(r['status'])}</td>"
        f"<td>{_esc(r['retest'])}</td></tr>" for r in risks)
    ctl_rows = "".join(
        f"<tr><td>{_esc(c['name'])}</td><td>{_esc(c['nist_ai_rmf'])}</td><td>{_esc(c['owasp'])}</td>"
        f"<td>{_esc(ev_by[c['evidence']]['proof'])}</td>"
        f"<td class='{'ok' if ev_by[c['evidence']]['status']=='passing' else 'warn'}'>{_esc(ev_by[c['evidence']]['status'])}</td></tr>"
        for c in controls)

    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Governance</title>
<style>
:root{{--bg:#f4f6fa;--panel:#fff;--line:#dce2ec;--ink:#141824;--muted:#5a6579;--accent:#2f5bd8;--ok:#1f8a5b;--warn:#b7791f;--bad:#c2334f;--f:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
@media(prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#0b0e14;--panel:#141a23;--line:#273040;--ink:#e9eef7;--muted:#93a0b2;--accent:#6f9bff;--ok:#46c98a;--warn:#e0a84a;--bad:#ff6b81;color-scheme:dark}}}}
:root[data-theme=dark]{{--bg:#0b0e14;--panel:#141a23;--line:#273040;--ink:#e9eef7;--muted:#93a0b2;--accent:#6f9bff;--ok:#46c98a;--warn:#e0a84a;--bad:#ff6b81;color-scheme:dark}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f);line-height:1.55}}
.wrap{{max-width:980px;margin:0 auto;padding:40px 20px 72px}}h1{{font-size:26px;margin:0 0 4px}}h2{{font-size:17px;margin:34px 0 12px}}
.sub{{color:var(--muted);margin:0}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:22px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}}.card .b{{font-size:30px;font-weight:700}}
.card .l{{color:var(--muted);font-size:13px}}table{{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:13.5px}}
th,td{{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}}th{{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}}
tr:last-child td{{border-bottom:none}}code{{font-family:ui-monospace,Menlo,monospace;font-size:12px}}.ok{{color:var(--ok)}}.warn{{color:var(--warn)}}.bad{{color:var(--bad);font-weight:600}}
.thread{{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:12px;padding:16px;font-size:14px}}
.thread b{{color:var(--accent)}}
</style></head><body><div class="wrap">
<h1>Northwind AI Security &amp; Governance</h1>
<p class="sub">Executive assurance view. Every risk traces to a control, every control to tested evidence.</p>
<div class="cards">
<div class="card"><div class="b">{len(inv)}</div><div class="l">AI systems in inventory</div></div>
<div class="card"><div class="b" style="color:var(--bad)">{tiers['critical']+tiers['high']}</div><div class="l">high/critical-tier systems</div></div>
<div class="card"><div class="b">{len(risks)}</div><div class="l">tracked risks</div></div>
<div class="card"><div class="b" style="color:{'var(--bad)' if open_risks else 'var(--ok)'}">{len(open_risks)}</div><div class="l">open risks needing action</div></div>
</div>
<h2>Risk register</h2>
<table><thead><tr><th>ID</th><th>Risk</th><th>OWASP</th><th>Impact</th><th>Status</th><th>Retest evidence</th></tr></thead><tbody>{risk_rows}</tbody></table>
<h2>Control mapping &amp; evidence</h2>
<table><thead><tr><th>Control</th><th>NIST AI RMF</th><th>OWASP</th><th>Proof</th><th>Evidence</th></tr></thead><tbody>{ctl_rows}</tbody></table>
<h2>Traceability thread</h2>
<div class="thread"><b>risk-001</b> (system-prompt leak, Project 1) &rarr; logged as a high/high risk &rarr;
mapped to <b>ctl-output-filter</b> (NIST MANAGE-2.2, OWASP LLM07) &rarr; tested by <b>ev-001</b>
(red-team runner) &rarr; proof: vulnerable 1/10 &rarr; defended 0/10 &rarr; status <b>mitigated</b>.
One technical weakness, followed all the way to a managed, evidenced business risk.</div>
</div></body></html>"""


def main() -> int:
    inv, risks = _load("inventory.json"), _load("risk_register.json")
    controls, evidence = _load("control_mapping.json"), _load("evidence.json")
    errors = validate(inv, risks, controls, evidence)
    if errors:
        print("TRACEABILITY ERRORS:")
        for e in errors:
            print("  -", e)
        return 1

    open_risks = [r for r in risks if r["status"] == "open"]
    lines = ["# Northwind AI Security & Governance", "",
             f"- AI systems: {len(inv)}  |  tracked risks: {len(risks)}  |  open: {len(open_risks)}",
             "", "## Risk register", "", "| ID | System | Risk | OWASP | Status | Evidence |",
             "| --- | --- | --- | --- | --- | --- |"]
    for r in risks:
        lines.append(f"| {r['id']} | {r['system']} | {r['title']} | {r['owasp']} | {r['status']} | {r['retest']} |")
    lines += ["", "## Open actions", ""]
    lines += [f"- {r['id']}: {r['title']} (control {r['control']})" for r in open_risks] or ["- none"]
    with open("GOVERNANCE.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    with open("dashboard.html", "w", encoding="utf-8") as fh:
        fh.write(build_dashboard(inv, risks, controls, evidence))
    print(f"Traceability OK. {len(inv)} systems, {len(risks)} risks, {len(open_risks)} open.")
    print("Wrote GOVERNANCE.md and dashboard.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
