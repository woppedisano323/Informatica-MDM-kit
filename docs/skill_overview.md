# MDM Kit — Skill Overview

Informatica Cloud MDM deployment kit for Business 360 / Customer 360 SaaS. Three skills that chain together across a full engagement — from use case alignment through source profiling to a verified golden record in the org.

---

## How the Skills Chain

```
Consultant runs /mdm-setup
  └─ Phase 1: Use case discovery
       Output: MDM_UseCase_<Client>.xlsx  →  stakeholder approval  →  PDF lock

  └─ Phase 2: Technical discovery workbook
       Output: MDM_Discovery_<Client>.xlsx  (9 sheets)

Consultant runs /mdm-profile <path/to/MDM_Discovery_<Client>.xlsx>
  └─ Source profiling in IDMC Data Profiling (one task per source)
  └─ Results interpretation + DQ analysis + CDI transformation plan
       Output: MDM_Profile_DQ_<Client>.xlsx
       Updates: Discovery Workbook sheets 5, 7, 9

Consultant runs /mdm-deploy <path/to/MDM_Discovery_<Client>.xlsx>
  └─ Pre-flight checks + conflict review
  └─ 9 deployment steps, one action at a time
       Output: MDM_Deployment_Steps_<Client>.xlsx + session PDF
```

Each skill gates the next. `/mdm-deploy` validates that Sheet 9 (Profiling Results) is populated before proceeding.

---

## /mdm-setup

**Purpose:** Use case alignment and technical discovery.

**Invocation:** `/mdm-setup`

**Phases:**

| Phase | What happens | Output |
|-------|-------------|--------|
| Phase 1 — Use Case | Business problem, source systems, deployment pattern | `MDM_UseCase_<Client>.xlsx` |
| Confirm | Lock approved use case | `MDM_UseCase_<Client>.pdf` + `MDM_Discovery_<Client>.xlsx` |
| Phase 2 — Discovery | Technical config: source systems, data model, survivorship, DQ, match model, CDI, success criteria | `MDM_Discovery_<Client>.xlsx` (9 sheets) |

**Discovery Workbook — 9 sheets:**

| Sheet | Contents |
|-------|----------|
| 1 — Use Case | Business objective, consumers, success definition, DQ problem, deployment pattern |
| 2 — Source Systems | Display name, internal ID (immutable warning), completeness, currency, recommended rank |
| 3 — Data Model | Custom field groups — field type, internal ID, source, Date vs DateTime decision, fgid plan |
| 4 — Survivorship | Source ranking + reasoning; decay rules (Max/Min score, Unit, Period) |
| 5 — DQ Planning | Per-field rule plan (Basic/Advanced/DaaS), severity, trust downgrade %, DaaS entitlement check, blank-canvas prereqs |
| 6 — Match Model | Custom match model (primary) or predefined match model decision, match criterion, strategy, population, M&M job name |
| 7 — Data Loading | CDI vs File Import; Secure Agent, connections, per-source mapping config, CDI expression notes |
| 8 — Success Criteria | Per-step verification checklist (9 steps) |
| 9 — Profiling Results | IDMC Data Profiling summary — completeness scores, DQ flags, key findings per source; gate check for /mdm-deploy |

**Test mode:** `/mdm-setup --test` — prefixes all artifacts and org values with `[TEST-NNN]` for traceability.

---

## /mdm-profile

**Purpose:** Source data profiling, DQ analysis, and CDI transformation planning.

**Invocation:** `/mdm-profile <path/to/MDM_Discovery_<Client>.xlsx>`

**Steps:**

| Step | What happens |
|------|-------------|
| P1 — Confirm Sources | Reads source systems from Discovery Workbook; confirms files are ready |
| P2 — Best Practices | Profiling guidance: all rows vs sample, one task per source, fields to watch |
| P3 — Create Tasks | Step-by-step IDMC Data Profiling task creation (includes column mismatch fix) |
| P4 — Run + Monitor | Run all tasks; confirm Succeeded status; diagnose failures |
| P5 — Export | Export results to Excel; confirm file naming |
| P6 — Interpret | Read exports; apply field-type heuristics (phone, name, date, state, postal, email, ID) |
| P7 — DQ Analysis | Map issues to MDM rule type, function, severity, trust downgrade % |
| P8 — CDI Transforms | Generate expression pseudocode per field per source |
| P9 — Survivorship | Rank sources by completeness evidence; provide rationale |
| P10 — Generate Workbook | Produce `MDM_Profile_DQ_<Client>.xlsx`; tell consultant what to copy back into Discovery Workbook |

**Profile/DQ Workbook — 7 sheets:**

| Sheet | Tab Color | Contents |
|-------|-----------|----------|
| Glossary | Gray | Profiling and DQ terms |
| Source 1/2/3 — Name | Blue | Per-field stats: null %, distinct %, pattern count, top pattern %, DQ flag, notes |
| DQ Analysis | Red | Issue → rule type → function → severity → trust downgrade % → EVO flag |
| CDI Transformations | Green | Source → field → CDI expression pseudocode → output example |
| Summary | Navy | Survivorship ranking, DQ rule counts, CDI summary, feed-back reference to Discovery Workbook |

**DQ Issue Flag logic:**
- 🔴 RED — null% > 10% or pattern count > 2
- 🟡 YELLOW — null% 1–10% or pattern count = 2
- ✅ GREEN — null% = 0% and pattern count ≤ 1

**Known IDMC profiling issues documented in the skill:**
1. Column count mismatch → 0-row output (fix: delete and recreate task)
2. Date inference false positive — `Date(year/dd/mm)` on clean YYYY-MM-DD data
3. Phone field inferred as Integer/Decimal — wrap with `TO_CHAR()` in CDI
4. Agent version warning (PowerCenter 10.2.0) — informational only

**Test mode:** `/mdm-profile --test` — prefixes workbook artifacts with `[TEST-NNN]`.

---

## /mdm-deploy

**Purpose:** Step-by-step deployment coaching in a live Business 360 / Customer 360 SaaS org.

**Invocation:** `/mdm-deploy <path/to/MDM_Discovery_<Client>.xlsx>`

**Pre-flight checks (before any steps):**
- Reads and validates Discovery Workbook (all required fields populated)
- UI review: confirm no source system ID collisions, no existing records in the deployment entity, no legacy M&M jobs
- Generates `MDM_Deployment_Steps_<Client>.xlsx` (write-once step reference workbook)

**9 Deployment Steps:**

| Step | Type | What happens |
|------|------|-------------|
| 1 — Source Systems | UI | Create one source system per source in B360 — display name + internal ID (permanent) |
| 2 — Extend Data Model | UI | Add custom field groups to the blank-canvas entity |
| 3 — Survivorship | UI | Configure source ranking + decay rules |
| 4 — Data Quality Rules | UI | Configure Basic, Advanced, and DaaS rules; set severity + trust downgrade % |
| 5 — Match Model | UI | PATH A (custom entity): create match model from scratch via Directed AI wizard, publish. PATH B (predefined entity): select existing match model. |
| 6 — Load Data | UI | File Import with sample CSVs (pre-deployment validation). CDI production pipeline is a separate downstream project. |
| 7 — Monitor Ingress | UI | Confirm all source ingress jobs Succeeded; verify record counts in C360 |
| 8 — Match and Merge | UI | Run M&M job; confirm job completes |
| 9 — Validate Golden Records | UI | Verify consolidation status, source record contributions, trust scores |

**Coaching format (every step):**
1. Orient — one sentence on what the step does and why it matters
2. Navigate — exact path from documented experience; describe the screen, give the action, ask Done?
3. Act — one action at a time; wait for response
4. React — diagnose unexpected state before continuing
5. Verify — confirm outcome before closing the step
6. Signoff — summary + name; session JSON and PDF updated

**Irreversible actions flagged before each step:**
- Source System Internal ID — permanent after creation
- Survivorship must be configured before records exist
- Match model must be Published before records are loaded
- Match rule cannot be edited after save
- Predefined assets cannot be deleted
- Custom field groups locked after records exist

---

## Key Architecture Decisions

| Decision | What | Why |
|----------|------|-----|
| Blank-canvas entity | Use B360 → New → Business Entity (not copy of c360.person) | Person copy inherits smart fields with DQ rule associations requiring dictionary privileges — causes silent load failures on all Picklist fields |
| File Import as pre-deployment validation | Sample CSVs loaded via C360 File Import before production pipeline | Validates entity config, DQ rules, match keys, and survivorship without requiring CDI setup. CDI production pipeline is a separate downstream project. |
| Survivorship before records | Configure ranking before first record loads | Trust scores not retroactively recalculated |
| Match model published before load | Publish before CDI ingress | Records loaded before publish have no match keys and will never be matched |
| EVO for DQ rules | Post-Oct 2025 orgs use Enrichment and Validation Orchestrator | Requires Enrichment Provider + Enrichment Scenario Group permissions in Administrator |
| DaaS Address Verification | Predefined rule — must be explicitly enabled | Disabled by default in blank-canvas entity; Address DaaS included in MDM SaaS, Phone/Email DaaS requires separate entitlement |

---

## Verified Test Run: PROFILE-TEST-001 (2026-10-27/28)

FSI scenario — three source systems, blank-canvas entity, CDI load, M&M verification.

**Sources:** ORION Wealth Management · ENCOMPASS Loan Origination · FiServ Core Banking

**Profiling findings confirmed:**
- ORION: phone 3 formats (dots/dashes/plain), state 3 variants, postal 5+4 mix, name ALL CAPS subset
- ENCOMPASS: birth_date 2 formats (MM/DD/YYYY 46% / YYYY-MM-DD 54%), 15% null phone, name casing
- FISERVER: phone 4 patterns + numeric inference, 13% null email, birth_date 2 formats, name casing

**CDI transforms applied:** INITCAP (names), REG_REPLACE (phone), IIF+TO_DATE (birth_date), IIF+UPPER+SUBSTR (state/postal)

**Survivorship ranking:** FiServ #1 · ENCOMPASS #2 · ORION #3

**MDM-TEST-001 results:** 32 source records → 17 golden records (15 merges). James Morrison: 3 contributing source records → 1 golden record confirmed.

See `examples/PROFILE-TEST-001/` for all source files and populated output workbook.
