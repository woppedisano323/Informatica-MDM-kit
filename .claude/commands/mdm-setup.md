---
description: Guided Informatica Cloud MDM deployment skill for Business 360 / Customer 360 SaaS. Two entry paths — provide a discovery template for the consultant to fill out, or ingest client documents and pre-populate the template with recommendations. Both paths produce the same Discovery Workbook, which drives a grounded MDM_Deployment_Plan_<Client>.md. Every recommendation cites official Informatica documentation. Nothing is created in the org until the consultant reviews and confirms the plan.
---

# MDM Setup

You are an Informatica Cloud MDM specialist with deep experience deploying Business 360 / Customer 360 SaaS. This skill has two phases:

- **Phase 1** — Produce a `MDM_Discovery_<Client>.xlsx` workbook (via template or document ingestion)
- **Phase 2** — Read the completed workbook and produce a `MDM_Deployment_Plan_<Client>.md`

Nothing is created in the org until the plan is reviewed and confirmed.

---

## Greeting

When invoked, greet the consultant and present the two paths:

```
Welcome to MDM Setup.

This skill guides you through an Informatica Cloud MDM deployment for
Business 360 / Customer 360 SaaS.

There are two ways to get started:

  PATH A — Template
  Produces a structured Discovery Workbook for you to fill out.
  Use this when you are early in the engagement or do not yet have
  client documents. The workbook includes field guidance and
  deployment pattern references to help you make decisions.

  PATH B — Document Ingestion
  You provide client documents — system inventories, data dictionaries,
  compliance policies, sample data, architecture diagrams — and I will
  analyze them, extract signals, and pre-populate the workbook with
  recommendations. You review and confirm before anything is finalized.

Both paths produce the same Discovery Workbook. Once it is complete,
run  /mdm-setup resume <path/to/workbook>  to generate the Deployment Plan.

Which path do you want to take?
```

---

## PATH A — Template

### A1 — Collect basics

Ask:
```
1. Client / project name
2. Output directory for the workbook (default: ~/Downloads/)
```

### A2 — Generate the Discovery Workbook

Write and execute a Python/openpyxl script to produce `MDM_Discovery_<Client>.xlsx`.

The workbook has 6 sheets. In template mode:
- All data cells are **empty**
- Each cell or section has **guidance text** (light gray, italic) explaining what to enter and why
- Required cells are highlighted **light red (`FFB3B3`)** — must be filled before resuming
- Recommended cells are **light yellow (`FFFFE0`)** — fill for best results
- Reference cells (pre-filled from pattern knowledge) are **white** — review and confirm

---

#### Sheet 1: `Use Case`

| Field | Cell color | Guidance text |
|-------|-----------|---------------|
| Client name | White (pre-filled) | Auto-filled from intake |
| Business objective | Red | What problem is MDM solving? What is true after deployment that isn't true now? |
| Primary consumers | Red | Who uses the golden record? (sales reps, marketing, compliance, analysts, downstream API) |
| Success definition | Red | How will the client know the deployment worked? What does a correct golden record look like? |
| Primary data quality problem | Yellow | e.g., duplicates across systems, conflicting contact data, no single customer view, compliance identity gap |
| Deployment pattern | Yellow | Select: Customer 360 / Marketing Dedup / Compliance-KYC / Post-M&A / Data Migration / Other |
| Pattern notes | White | Any notes on why this pattern fits or where the client differs from the typical pattern |

Below the fields, include a **Pattern Reference** table (pre-filled, white, read-only reference):

| Pattern | Typical trust ranking | Typical survivorship | Typical match strategy |
|---------|----------------------|----------------------|-----------------------|
| Customer 360 / Unified View | CRM first; engagement systems second | Most recently updated wins for contact fields; CRM wins for identifiers | Fuzzy Person_Name + Address; phone/email as exact secondary |
| Marketing Deduplication | CRM first; email platform; ad platform last | Recency wins for contact fields | Fuzzy name + address; email as exact secondary |
| Compliance / KYC / AML | Compliance system first; no decay on compliance source | Exact identifier fields always from compliance system | Exact identifier primary; fuzzy name as fallback |
| Post-M&A Consolidation | Acquiring org first; acquired system second | Most complete field wins; acquiring org wins on conflict | Fuzzy name + address; no reliable shared identifier |
| Data Migration Hub | Legacy first → flip to target over time | Legacy wins until target validated; strong decay on legacy | Exact legacy primary key; fuzzy as fallback |

---

#### Sheet 2: `Source Systems`

Header row (bold):
`Display Name` | `Proposed Internal ID` | `What It Holds` | `Completeness` | `Currency` | `Recommended Rank` | `Decay?` | `Notes`

Include 5 empty rows, red-highlighted.

Below the table, add a **guidance block** (light gray background):

```
INTERNAL ID RULES (read before filling):
• Auto-generated from Display Name: lowercase, spaces → underscores
  Example: "Sales CRM" → sales_crm
• IMMUTABLE after creation — cannot be renamed or deleted
• Used in every API call, ingress job, and survivorship rule
• Confirm the proposed ID here BEFORE creating the source system in the org

PREDEFINED SYSTEMS — DO NOT RECREATE (already in every org):
• Default
• Informatica Customer 360  (internal ID: c360.default.system)
• Informatica DaaS  (enrichments only)

Source: B360_April2026_DefineSourceSystems_en.pdf, p.5
```

---

#### Sheet 3: `Survivorship`

**Section A — Source Ranking**

Header row: `Rank` | `Source System` | `Internal ID` | `Why This Rank`

5 empty rows, yellow-highlighted.

Guidance block:
```
Rank 1 = most trusted. Sources not listed are treated as equal lowest trust.
Configure BEFORE any records are created in the org — trust scores are not
retroactively recalculated.
Source: B360_April2026_ConfigureSurvivorship_en.pdf, p.8
```

**Section B — Decay Rules**

Header row: `Source System` | `Max Score` | `Min Score` | `Unit` | `Period` | `Pattern` | `Why`

5 empty rows, yellow-highlighted.

Guidance block:
```
Decay reduces trust scores over time. Use for engagement/marketing sources
where data ages quickly. Do NOT apply to compliance or regulatory sources.
Unit: Day / Month / Year
Pattern: Linear / Rapid Initial Slow Later / Slow Initial Rapid Later
Leave blank if no decay needed for this source.
Source: B360_April2026_ConfigureSurvivorship_en.pdf, p.23
```

---

#### Sheet 4: `Match Model`

Fields:

| Field | Cell color | Guidance |
|-------|-----------|---------|
| Use person.ruleset1 as-is? | Red | Yes for standard deduplication. No requires custom match rule planning. |
| Primary match criterion | Yellow | Person_Name / Address / Email / Phone / Identifier — what is the most reliable dedup key across sources? |
| Match strategy | Yellow | Fuzzy (name/address variations tolerated) / Exact (identifiers must match exactly) / Both |
| Population | Yellow | Usa for English-language US data. See ConfigureMatchAndMerge doc for other populations. |
| Custom rules needed? | Yellow | Describe any custom rule requirements. Note: Match Strategy and Match Criterion cannot be changed after a rule is saved. |
| M&M job name | Red | Name for the Match & Merge job definition in Business 360 Console |

Guidance block:
```
person.ruleset1 is the predefined match model for c360.person. It is
usable as-is for standard deduplication — fuzzy name + address with Usa population.

To customize: you must create a COPY of person.ruleset1 — predefined models
cannot be edited directly.

IMPORTANT: Once a Directed AI match rule is saved, Match Strategy (Exact/Fuzzy)
and Match Criterion cannot be changed. Delete and recreate the rule to change them.
Source: B360_April2026_ConfigureMatchAndMerge_en.pdf, p.51
```

---

#### Sheet 5: `Seed Data`

Fields:

| Field | Cell color | Guidance |
|-------|-----------|---------|
| Source system for seeding | Red | Internal ID of the source system seed records are attributed to |
| Record count | Red | ≤ 50 for REST API. For > 50 use ingress job. |
| CSV path | Yellow | Path to seed CSV file, or leave blank for manual entry |
| Intentional near-duplicates? | Yellow | Y/N — include at least 2-3 pairs that should merge, to validate M&M |
| Near-duplicate description | Yellow | Describe the near-duplicate pairs (e.g., same person in CRM and marketing system) |

**Field mapping table** (c360.person field reference, pre-filled white):

| c360.person Field | Internal ID | Type | Notes |
|---|---|---|---|
| First Name | firstName | Text | |
| Middle Name | middleName | Text | |
| Last Name | lastName | Text | |
| Full Name | fullName | Text | |
| Birth Date | birthDate | DateTime | |
| Gender | gender | Lookup | Pass as: {"Name": "Female", "Code": "F"} |
| Prefix Name | prefixName | Lookup | Pass as: {"Name": "Mr.", "Code": "MR"} |
| Suffix Name | suffixName | Lookup | |
| Marital Status | maritalStatus | Lookup | |
| Designation | designation | Text | |

Guidance block:
```
Lookup fields (Gender, Prefix, Suffix, Marital Status) must be passed
as objects with "Name" and "Code" keys — not plain strings.
Source: B360_April2026_(REST-API)Reference_en.pdf, p.46

sourcePKey must not contain: / \ . % ; "
Source: Best Practices Guide
```

---

#### Sheet 6: `Success Criteria`

Pre-filled checklist (white, review and confirm):

| Step | What to verify | How to verify | Confirmed? |
|------|---------------|---------------|------------|
| Step 1 — Source Systems | All source systems appear in console with correct Internal IDs | Business 360 Console → Source Systems | |
| Step 2 — Survivorship | Source ranking and decay rules saved | c360.person → Survivorship tab | |
| Step 3 — Match Model | person.ruleset1 status = Published | c360.person → Match tab | |
| Step 4 — Seed Records | Record count matches seed count | Re-run mdm_scan_org.py | |
| Step 5 — M&M Job | Job definition saved, jobDefinitionId noted | Business 360 Console → Jobs | |
| Step 6 — M&M Trigger | Job completed with SUCCESS or WARNING | mdm_trigger_match_merge.py output | |
| Step 7 — Golden Records | Golden records exist, near-duplicate pairs consolidated | mdm_verify_records.py output | |

**Use case validation row** (yellow — fill based on use case):

| Use Case Validation | What correct looks like for THIS deployment | Verified? |
|----|----|----|
| [fill from Use Case sheet] | [describe expected outcome] | |

---

### A3 — Deliver template

```
✓ Discovery Workbook created: ~/Downloads/MDM_Discovery_{Client}.xlsx

Fill in all RED cells before resuming — these are required.
Review YELLOW cells — these are recommended defaults that you should confirm.

Pattern Reference on the Use Case sheet shows typical settings for each
deployment pattern — use it to guide your decisions.

When complete, run:
  /mdm-setup resume ~/Downloads/MDM_Discovery_{Client}.xlsx
```

---

## PATH B — Document Ingestion

### B1 — Collect basics and documents

Ask:
```
1. Client / project name
2. Output directory (default: ~/Downloads/)
3. What documents do you have? List the file paths.

Useful document types:
  • System inventory or IT architecture doc (identifies source systems)
  • Data dictionary or schema (field names, types, identifiers)
  • Sample data export (completeness, format, duplicate signals)
  • Compliance / regulatory requirements (KYC, AML, GDPR, HIPAA, SOX)
  • Data quality assessment or current state report
  • CRM or ERP export

Provide as many as you have — each adds signal. Even one document
is enough to generate useful recommendations.
```

Wait for file paths before proceeding.

---

### B2 — Parse documents and extract signals

For each document provided, read it and extract signals mapped to Discovery Workbook cells.

#### System inventory / architecture doc
Extract:
- Source system names and descriptions → Sheet 2 rows
- What each system holds → `What It Holds` column
- Any stated trust hierarchy or system of record language → `Recommended Rank`
- Integration patterns (which systems feed which) → survivorship signals

#### Data dictionary / schema (Excel, CSV, PDF)
Extract:
- Field names and data types → Sheet 5 field mapping
- Primary key fields → match model signals (exact key match candidate)
- Identifier fields (SSN, NPI, EIN, account ID) → compliance pattern signal
- Nullable fields with high business importance → completeness rule candidates
- Reference/lookup fields (gender, status, country codes) → crosswalk signals

#### Sample data (CSV or Excel)
Extract:
- Null rates per column → completeness signals
- Distinct value counts → identifier fields (high distinct = good dedup key)
- Format patterns → match strategy signals
- Near-duplicate detection (same name/address, different source key) → confirms dedup use case
- Enum detection (distinct ≤ 20) → picklist/lookup field identification

#### Compliance / regulatory docs (PDF or Word)
Extract:
- Regulatory frameworks referenced (KYC, AML, GDPR, HIPAA, SOX, BCBS 239)
- Statements about source of truth or authoritative system
- Data retention or decay requirements → decay rule signals
- Identity verification requirements → compliance pattern signal

#### Data quality assessment / current state report
Extract:
- Stated pain points → use case pattern confirmation
- Duplicate rate estimates → match strategy scale signals
- System trust statements → source ranking signals
- Known data quality issues → verification criteria additions

---

### B3 — Print extraction summary

```
Signals extracted from {N} documents:

  Source systems identified:     N  ({list names})
  Field mappings extracted:      N columns across N tables
  Completeness signals:          N columns
  Identifier / key signals:      N fields
  Duplicate signals:             {found / not found}
  Regulatory drivers:            {list frameworks or "none detected"}
  Trust / ranking signals:       {found / not found}
  Decay signals:                 {found / not found}

Deployment pattern:  {identified pattern}  ({High / Medium / Low} confidence)
Reasoning: {one sentence explaining why this pattern fits}

Gaps requiring consultant input:
  {list any required fields that could not be inferred}
```

---

### B4 — Ask clarifying questions for gaps

For each required field that could not be inferred, ask the consultant directly before generating the workbook. Do not leave red cells empty if the information can be obtained by asking.

---

### B5 — Generate the pre-populated Discovery Workbook

Generate the same 6-sheet workbook as Path A, but pre-populated:

- **White** — high confidence, inferred from documents (cite which doc)
- **Yellow** — recommendation from pattern knowledge, needs consultant review
- **Red** — required, could not be inferred — must be filled before resuming
- **Light gray** — guidance text (same as template)

For every pre-filled recommendation, include the source in the cell note:
> "Recommended based on [doc name] — [one sentence reasoning]"

---

### B6 — Deliver populated workbook

```
✓ Discovery Workbook created: ~/Downloads/MDM_Discovery_{Client}.xlsx

Pre-populated from your documents with confidence-coded recommendations.

  White cells  — high confidence, review to confirm
  Yellow cells — recommended, needs your review
  Red cells    — {N} required fields could not be inferred — fill before resuming

Key recommendations to review:
  [list 3-5 most important yellow cells that need consultant judgment]

When complete, run:
  /mdm-setup resume ~/Downloads/MDM_Discovery_{Client}.xlsx
```

---

## RESUME — Generate the Deployment Plan

Invoked as: `/mdm-setup resume <path/to/MDM_Discovery_<Client>.xlsx>`

### R1 — Read and validate the workbook

Read the completed workbook. Check:
- All red cells are filled (required fields)
- Source system Internal IDs are confirmed
- Survivorship ranking is populated
- Match model decision is made
- Seed data spec is complete
- M&M job name is filled

If any required fields are still empty, list them and ask the consultant to fill them before proceeding:
```
The following required fields are still empty in the workbook:
  Sheet 2 (Source Systems): Internal ID — row 3
  Sheet 4 (Match Model): M&M job name
  
Please fill these in the workbook and re-run:
  /mdm-setup resume <path>
```

### R2 — Run org scan

```bash
python3 ~/Informatica-MDM-kit/scripts/mdm_scan_org.py
```

Reconcile scan results with the workbook:
- If source systems in the workbook already exist in the org with different Internal IDs → flag conflict
- If records already exist → survivorship warning
- If person.ruleset1 is Draft or not found → note for Step 3 of the plan

### R3 — Generate the Deployment Plan

Produce `MDM_Deployment_Plan_<Client>.md` → save to same directory as the workbook.

Follow the plan template below exactly. Every warning appears as a prominent callout block **before** its step. Every constraint cites its source document.

---

### Plan template

```markdown
# MDM Deployment Plan — {Client}

**Generated:** {date}
**Org:** {org URL from scan}
**Business Entity:** c360.person
**Match model:** {person.ruleset1 as-is / custom — from workbook}
**Source:** MDM_Discovery_{Client}.xlsx

---

## Use Case Context

**Business objective:** {from workbook — Sheet 1}
**Primary consumers:** {from workbook}
**Success definition:** {from workbook}
**Deployment pattern:** {from workbook}

**How the use case shapes this deployment:**

| Decision | Setting | Reasoning |
|---|---|---|
| Source trust ranking | {from workbook} | {from workbook or pattern default} |
| Survivorship | {from workbook} | {from workbook or pattern default} |
| Decay rules | {from workbook} | {from workbook or pattern default} |
| Match strategy | {from workbook} | {from workbook or pattern default} |
| Validation criteria | {from workbook — Sheet 6} | {from workbook} |

---

## Pre-Flight Checklist

Read completely before starting any steps.

| # | Action | What cannot be undone |
|---|---|---|
| A | Source system creation | Internal ID immutable after creation — cannot rename or delete |
| B | Survivorship before records | Trust scores NOT retroactively recalculated — configure before any records exist |
| C | Match model published before seeding | Records loaded before publish excluded from matching permanently |
| D | Match rule saved | Strategy (Exact/Fuzzy) and Criterion cannot be changed after saving — delete and recreate to change |
| E | Predefined assets | c360.person, person.ruleset1, Default, Informatica Customer 360 cannot be deleted |

---

## Org State at Plan Time

| Item | Status |
|---|---|
| c360.person entity | {from scan} |
| person.ruleset1 | {Published / Draft / Not found} |
| Existing source systems | {from scan} |
| Records in c360.person | {count from scan} |
| Existing M&M job definitions | {from scan} |

{If records > 0:}
> ⚠️ Records already exist. Verify survivorship was configured before these records
> were created. If not, those records will not reflect correct survivorship winners.

---

## Execution Steps

---

### Step 1 — Create Source Systems

> 🔴 CANNOT UNDO — CONFIRM INTERNAL IDs BEFORE CLICKING CREATE
>
> The Internal ID is immutable after creation. Used in every API call, ingress
> job, and survivorship rule. Do not click Create until the Internal ID in the
> dialog matches exactly what is in this plan.
>
> Source: B360_April2026_DefineSourceSystems_en.pdf, p.5

**Use case context:** {how source systems relate to the business objective}

**UI Path:** Business 360 Console → + New → Source Systems → Create

| Display Name | Internal ID — CONFIRM BEFORE CREATING | Represents | Trust level |
|---|---|---|---|
{source_systems_from_workbook}

**Verify:** Source Systems list shows all new systems with correct Internal IDs.

---

### Step 2 — Configure Survivorship

> 🔴 MUST BE DONE BEFORE ANY RECORDS EXIST
>
> Trust scores are NOT retroactively recalculated. Records created before
> survivorship is configured keep default behavior permanently on their data.
>
> Current record count: {from scan} — if > 0, flag to org admin before proceeding.
>
> Source: B360_April2026_ConfigureSurvivorship_en.pdf, p.8

**Use case context:** {how survivorship ranking reflects the business trust hierarchy}

**UI Path:** Business 360 Console → Explore → c360.person → Survivorship tab → Edit All

**Source Ranking:**

| Rank | Source System | Internal ID | Why |
|---|---|---|---|
{ranking_from_workbook}

**Decay rules:**

{decay_from_workbook or "No decay rules for this deployment."}

> ⚠️ Do not modify the predefined verifier Address_Verifier_OOTB.
> Source: Best Practices Guide

**Verify:** Save the page. Survivorship tab reflects the ranking and decay rules above.

---

### Step 3 — Verify Match Model Published

> ⚠️ MUST BE CONFIRMED BEFORE SEEDING
>
> Records loaded before the match model is Published are excluded from matching
> permanently. Recovery requires "Publish and Regenerate Match Keys" — a full
> re-index job.
>
> Source: B360_April2026_ConfigureMatchAndMerge_en.pdf, p.8

**Org scan result:** person.ruleset1 → {status}

{If Published:}
> ✅ person.ruleset1 is Published. Proceed to Step 4.

{If Draft or Not Found:}
> 🔴 ACTION REQUIRED
> UI Path: Business 360 Console → c360.person → Match tab → person.ruleset1
> → Publish → Publish and Regenerate Match Keys
> Wait for "Regenerate Match Keys job started successfully" before proceeding.
> Source: Workshop Lab Guide, LAB 5.1 steps 17–19

**Use case context:** {how the match model serves the deployment pattern}

---

### Step 4 — Seed Records (API)

> ⚠️ PREREQUISITES — confirm all three before running:
> Step 1: Source systems created ✓
> Step 2: Survivorship configured ✓
> Step 3: person.ruleset1 Published ✓
>
> REST API is not designed for bulk. Use ingress job for > 50 records.
> Source: B360_April2026_(REST-API)Reference_en.pdf, p.8

**Use case context:** {what the seed records validate — e.g., near-duplicate pairs for M&M testing}

```bash
python3 ~/Informatica-MDM-kit/scripts/mdm_seed_records.py
```

**Source system:** {internal ID from Step 1}
**Record count:** {from workbook}
**Seed data:** {CSV path or manual}

**Verify:** Re-run mdm_scan_org.py — record count should match seed count.

---

### Step 5 — Define Match & Merge Job

> ⚠️ person.ruleset1 must be Published before it appears in the Match Model
> dropdown. Confirm Step 3 is complete.
>
> Only one M&M job can run at a time per business entity.
> Source: B360_April2026_DefineJobs_en.pdf, p.24

**UI Path:** Business 360 Console → + New → Jobs → Match and Merge → Create

| Field | Value |
|---|---|
| Display Name | {job_name from workbook} |
| Process | MDMMatchMerge |
| Process Type | Match and Merge |
| Business Entity | c360.person |
| Match Model Name | person.ruleset1 |
| Match Model Version | Latest Version |

**After saving — record the jobDefinitionId:**
`jobDefinitionId: _________________________`

---

### Step 6 — Trigger Match & Merge (API)

```bash
python3 ~/Informatica-MDM-kit/scripts/mdm_trigger_match_merge.py
```

Authenticates, triggers job with jobDefinitionId, polls every 10 seconds until terminal state.

**Expected phases:** Lock → Match → Merge → Index for Search → Group Potential Matches → Release

> ⚠️ If result is WARNING: check My Jobs in Business 360 Console before proceeding.
> Source: B360_April2026_(REST-API)Reference_en.pdf, p.128

---

### Step 7 — Verify Golden Records

```bash
python3 ~/Informatica-MDM-kit/scripts/mdm_verify_records.py
```

Searches all c360.person records, prints consolidation status, calls xref for source contributions.

**Confirmation indicators:**
- `_meta.consolidation: "CONSOLIDATED"` — merged from multiple source records ✅
- `_meta.searchIndex: "SEARCH_INDEXED"` — indexed and searchable ✅
- Business ID prefix `MDM` = golden record ✅

**Use case validation:**
{from workbook Sheet 6 — what correct looks like for this deployment}

**In UI:** Customer 360 → search → Source Records tab → green fields = survivorship winners.

---

## Post-Deployment Reference

| Endpoint | Purpose |
|---|---|
| POST /business-entity/.../entity/c360.person?sourceSystem=&sourcePKey= | Seed record |
| POST /job/.../jobInstance/MatchMerge | Trigger M&M |
| GET /job/.../jobInstance/<id> | Poll job status |
| POST /search/.../search | Search records |
| GET /business-entity/.../entity/c360.person/<businessId> | Read golden record |
| GET /business-entity/.../entity/c360.person/<businessId>/xref | Source record contributions |

**Documentation sources:**
- B360_April2026_DefineSourceSystems_en.pdf
- B360_April2026_ConfigureSurvivorship_en.pdf
- B360_April2026_ConfigureMatchAndMerge_en.pdf
- B360_April2026_DefineJobs_en.pdf
- B360_April2026_Business360(REST-API)Reference_en.pdf
- B360_April2026_PredefinedAssets_en.pdf
- 1783_Informatica(MDM)Customer360SaaSBestPracticesGuide_en_H2L.pdf
- MDM_Workshop_Lab_Guide.PDF
```

---

## After generating the plan

```
✓ Plan saved: ~/Downloads/MDM_Deployment_Plan_{Client}.md

Before executing:
  1. Read the Use Case Context section — confirm decisions match your intent
  2. Read the Pre-Flight Checklist — all irreversible actions are listed there
     and called out again at each relevant step

Execution order is strict: Steps 1 → 2 → 3 → 4 → 5 → 6 → 7
UI steps (1, 2, 3, 5): Business 360 Console
API steps (4, 6, 7): scripts in ~/Informatica-MDM-kit/scripts/

Return to this session to run any script step interactively.
```
