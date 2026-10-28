# Informatica MDM Kit

Guided deployment skills for Informatica Cloud MDM — Business 360 / Customer 360 SaaS.

Three skills chain together to take a blank org from use case through profiling to a verified golden record.

---

## Skill Architecture

```
/mdm-setup    Phase 1 + 2   Use Case Alignment → Discovery Workbook
/mdm-profile  Profiling     Source Profiling → DQ Analysis → CDI Transforms
/mdm-deploy   Phase 3       Step-by-step Deployment Coaching
```

Each skill produces a shareable artifact and gates the next step. Nothing is created in the org until the consultant confirms each action.

---

## Skills

### `/mdm-setup`

**Phases 1 and 2.** Captures the business use case, identifies the deployment pattern, and produces two artifacts:

1. `MDM_UseCase_<Client>.xlsx` — use case alignment doc for stakeholder approval; lock as PDF with `/mdm-setup confirm <path>`
2. `MDM_Discovery_<Client>.xlsx` — 9-sheet technical workbook covering source systems, data model, survivorship, DQ planning, match model, data loading, success criteria, and profiling results

Run next: `/mdm-profile <path/to/MDM_Discovery_<Client>.xlsx>`

---

### `/mdm-profile`

**Source Profiling and DQ Analysis.** Runs between `/mdm-setup` and `/mdm-deploy`. Reads source systems from the Discovery Workbook, coaches IDMC Data Profiling setup and execution, interprets results, and produces:

1. `MDM_Profile_DQ_<Client>.xlsx` — per-source profiling stats, DQ Analysis, CDI transformation pseudocode, survivorship ranking recommendation

Results feed back into Discovery Workbook sheets 5 (DQ Planning), 7 (Data Loading), and 9 (Profiling Results) — which are gate checks in `/mdm-deploy`.

Run next: `/mdm-deploy <path/to/MDM_Discovery_<Client>.xlsx>`

---

### `/mdm-deploy`

**Phase 3 — Deployment Coach.** Reads the completed Discovery Workbook, runs a read-only org scan, validates pre-flight conditions, then walks through all 9 deployment steps using micro-step coaching (one action at a time, wait for confirmation before advancing):

1. Source Systems
2. Extend Data Model
3. Survivorship
4. Data Quality Rules
5. Match Model
6. CDI Ingress — Source 1
7. CDI Ingress — Sources 2 + 3
8. Match and Merge
9. Validate Golden Records

Produces `MDM_Deployment_Steps_<Client>.xlsx` + session PDF signed off after each step.

---

## Templates

Blank workbooks for starting a new engagement — copy and rename with the client name.

| File | Use |
|------|-----|
| `templates/MDM_Discovery_Template.xlsx` | Fill during `/mdm-setup` Phase 2 |
| `templates/MDM_Profile_DQ_Template.xlsx` | Populated automatically by `/mdm-profile` |

---

## Examples

Reference run: `examples/PROFILE-TEST-001/`

FSI scenario with three source systems (ORION wealth management, ENCOMPASS loan origination, FiServ core banking). 100-row dirty source files with deliberate DQ issues — designed to demonstrate all profiling findings and CDI transformation recommendations.

| File | Contents |
|------|----------|
| `MDM-PROFILE-TEST-001-20261027_ORION_CLIENTS_DIRTY.csv` | 100 rows — phone format mix, state variants, postal 5+4 |
| `MDM-PROFILE-TEST-001-20261027_ENCOMPASS_LOAN_CUSTOMERS_DIRTY.csv` | 100 rows — mixed birth_date formats, 15% null phone |
| `MDM-PROFILE-TEST-001-20261027_FISERVER_CUSTOMERS_DIRTY.csv` | 100 rows — phone as numeric, 13% null email, mixed birth_date |
| `MDM_Profile_DQ_FSI.xlsx` | Populated profile/DQ workbook from actual IDMC profiling runs |

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/mdm_scan_org.py` | Read-only org scan — entity status, match model, source systems, record count, job definitions |
| `scripts/mdm_session_pdf.py` | Regenerate deployment session PDF from session JSON — called after every step signoff |

---

## Supported Deployment Patterns

| Pattern | Use case |
|---------|---------|
| Customer 360 / Unified View | One view of the customer across CRM, support, and engagement systems |
| Marketing Deduplication | Clean customer lists before campaigns; dedup across email, CRM, and ad platforms |
| Compliance / KYC / AML | Verified customer identity linked by regulatory identifiers |
| Post-M&A Consolidation | Merge customer records from two companies after acquisition |
| Data Migration Hub | Cleansing layer before cutover to a new platform |

---

## Prerequisites

- Informatica Cloud MDM org with Customer 360 SaaS provisioned
- Secure Agent installed, running, and connected to IDMC
- Python 3 with `openpyxl` and `reportlab` (`pip install openpyxl reportlab`)
- IDMC username and password

---

## Usage

Open this repo in Claude Code, then:

```
/mdm-setup
```

Follow the three-skill sequence. Each skill tells you when to move to the next one.

---

## Documentation Basis

All recommendations cite official Informatica documentation:

- B360 April 2026: DefineSourceSystems, DefineJobs, ConfigureSurvivorship, ConfigureMatchAndMerge, DefineTheDataModel, REST API Reference, PredefinedAssets
- C360 April 2026: Customer 360 SaaS (File Import, Business Application)
- Informatica MDM Customer 360 SaaS Best Practices Guide (Aug 2024)
- B360 Workshop Lab Guide (Jun 2025)
