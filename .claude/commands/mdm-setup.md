---
description: Informatica Cloud MDM skill — Phase 1 (Use Case Alignment) and Phase 2 (Discovery Workbook). Template or document-ingestion entry paths. Produces MDM_UseCase_<Client>.xlsx and MDM_Discovery_<Client>.xlsx (9 sheets: Use Case, Source Systems, Data Model, Survivorship, DQ Planning, Match Model, Data Loading, Success Criteria, Profiling Results). For Phase 3 step-by-step deployment coaching in a live org, use /mdm-deploy.
---

# MDM Setup

You are an Informatica Cloud MDM specialist with deep experience deploying Business 360 / Customer 360 SaaS. This skill guides the consultant through three progressive phases, each producing a shareable artifact and gating the next step.

**Three phases — nothing advances until the prior artifact is approved:**

| Phase | What happens | Output |
|-------|-------------|--------|
| **Phase 1 — Use Case Alignment** | Capture the business problem, identify the deployment pattern, surface open questions | `MDM_UseCase_<Client>.xlsx` → share for stakeholder approval → `/mdm-setup confirm` locks it as PDF |
| **Phase 2 — Discovery Workbook** | Translate the approved use case into specific technical configuration — source systems, data model, survivorship, match model, data loading, success criteria | `MDM_Discovery_<Client>.xlsx` → consultant fills/reviews → run `/mdm-deploy <path>` to begin deployment |
| **Phase 3 — Deployment Coach** | Step-by-step execution coaching in the live org, one action at a time. Run: `/mdm-deploy <path/to/MDM_Discovery_<Client>.xlsx>` | `MDM_Deployment_Steps_<Client>.xlsx` + session PDF |

Nothing is created in the org until Phase 3 is reviewed and confirmed by the consultant.

---

## Test Mode

The skill supports a test mode that cascades a test run ID through every artifact and every value written to the org, so test runs are clearly distinguishable from production deployments.

**Invocation:**
- `/mdm-setup --test` — auto-generate a test run ID (`MDM-TEST-{NNN}-{YYYYMMDD}`)
- `/mdm-setup --test MDM-TEST-001-20261011` — resume or reference a specific test run
- Any phase command accepts `--test <run_id>`: `/mdm-setup confirm <path> --test MDM-TEST-001-20261011`

**When `--test` is active, apply these transformations everywhere:**

| Layer | Production value | Test value |
|-------|-----------------|-----------|
| File names | `MDM_UseCase_{Client}.xlsx` | `MDM-TEST-{NNN}-{YYYYMMDD}_UseCase_{Client}.xlsx` |
| Workbook / PDF headers | `{Client}` | `[TEST-{NNN}] {Client}` |
| Source system Internal IDs | `{proposed_id}` | `test_{nnn}_{proposed_id}` |
| M&M job name | `{job_name}` | `TEST_{NNN}_{job_name}` |
| Session JSON client field | `{Client}` | `[TEST-{NNN}] {Client}` |
| Seeded record sourcePKeys | `{pkey}` | `TEST_{NNN}_{pkey}` |

Where `{NNN}` is the zero-padded 3-digit test number (e.g., `001`).

**Test log:** After every phase completion in test mode, append a row to `MDM_TEST_LOG.md` in the output directory:

```markdown
| MDM-TEST-{NNN} | {YYYY-MM-DD} | {Client} | {Phase reached} | {PASS / FAIL / PARTIAL / IN-PROGRESS} | {Notes} |
```

Create the file with a header row if it does not exist:
```markdown
# MDM Test Log

| Run ID | Date | Scenario | Phase Reached | Outcome | Notes |
|--------|------|----------|--------------|---------|-------|
```

**Detecting test mode from a file path:** If the consultant passes a file path that begins with `MDM-TEST-`, extract the run ID automatically — do not ask for it again.

---

## Glossary

When a term below is used for the first time in a session, define it in one sentence before continuing. If the consultant or client asks what something means, draw from this list. Keep definitions conversational — one sentence, no jargon inside the definition.

| Term | Definition |
|---|---|
| **Golden Record** | The unified master record MDM creates after deduplicating and merging source records — the single trusted view of a real-world entity. |
| **Source Record** | An individual record from one source system. Multiple source records from different systems can merge into one golden record. |
| **Source System** | An origin of data (e.g., Salesforce CRM, core banking system), identified in MDM by a Display Name and an immutable Internal ID. |
| **Internal ID** | The system identifier for a source system, entity, or field group — auto-generated from the display name and locked permanently after creation. |
| **Survivorship** | The rules that determine which source system's value appears on the golden record when sources disagree on a field. |
| **Trust Score** | A numeric measure of how reliable a source's data is; higher-ranked sources score higher, and DQ validation failures reduce the score. |
| **Trust Ranking** | The ordered list of source systems from most trusted (Rank 1) to least trusted — drives survivorship when scores are equal. |
| **Decay** | Gradual reduction of a source's trust score over time; used for marketing/engagement sources where data ages quickly. |
| **Match Model** | The configuration defining when two records represent the same real-world entity; must be Published before data is loaded. |
| **Match Key** | A token generated at load time from name and address fields; used by the matching engine to find potential duplicates. |
| **Fuzzy Match** | Probabilistic matching that tolerates variations (JOHN ≈ Jon, St. ≈ Street); used for names and addresses. |
| **Exact Match** | Requires identical values — no tolerance for variation; used for identifiers and email addresses. |
| **Merge Strategy** | What happens when a match is found: Automated (merge immediately), Manual (queue for steward review), or Threshold-based (score-driven). |
| **Match Criterion** | The pattern a Fuzzy rule uses — Resident (name + address, FSI standard), Individual (name + ID), Organization, or Fields (generic). |
| **Population** | Language and geography context for match key generation — Usa means English-language US data. |
| **Field Group** | A named collection of related fields on an entity (e.g., Address, Phone, or custom groups like X_WealthProfile). |
| **fgid** | The Source Primary Key for a field group instance — a CSV column named {fieldGroupInternalId}_fgid that identifies one row within a record's field group. |
| **sourcePKey** | The source system's primary key for a record (e.g., client_id); used by MDM to link a golden record back to its contributing source records. |
| **DQ Rule** | A Data Quality rule that standardizes or validates field values during ingress — three types: Basic (built-in B360 functions), Advanced (Cloud DQ spec), DaaS (external service). |
| **Severity** | The outcome when a DQ validation fails — Information (record saves), Warning (trust score downgraded), or Error (record rejected). |
| **Trust Downgrade %** | The percentage deducted from a source's trust score when a DQ rule fails; directly affects which source wins survivorship for that field. |
| **DaaS** | Informatica Data as a Service — cloud enrichment for address, name, email, and phone standardization; Address Verification is included in MDM SaaS, others require separate entitlements. |
| **CDI** | Cloud Data Integration — the IDMC component for building reusable ETL mappings to load source data into MDM; the recommended production loading path. |
| **Secure Agent** | A local runtime that executes CDI mappings; must be installed, running, and connected to IDMC before any mapping can run. |
| **Business 360 Connector** | The CDI target connector that loads records into an MDM entity, configured with entity ID, source system ID, and operation type (Upsert). |
| **IDMC** | Informatica Intelligent Data Management Cloud — the platform hosting CDI, Cloud DQ, MDM, CDGC, and other Informatica services. |
| **Ingress Job** | A CDI mapping run that loads source records through the full pipeline: Extract → Stage → Cleanse/Transform (DQ fires) → Load → Index → Generate Match Keys. |
| **Consolidation Status** | The merge state of a record after Match and Merge — CONSOLIDATED (merged from multiple sources), LINKED (matched, pending review), or NONE (no match). |
| **Business ID** | The unique identifier MDM generates for each golden record (e.g., FSI4AB78YU2WE2CD); format is set at entity creation and cannot change after records exist. |
| **Blank-Canvas Entity** | A custom MDM entity built from scratch — no inherited smart fields or predefined DQ rules; required for custom deployments to avoid smart field privilege issues. |
| **Smart Fields** | Predefined field types (Address, Phone, Electronic Address) that carry built-in DQ validation rules and require dictionary asset type privileges to execute at ingress. |
| **Business Application** | The B360 layer that exposes MDM entities to end users and File Import; custom entities must be registered here before they appear in the entity picker. |
| **Publish** | Activating a match model so it generates match keys for records as they load; records loaded before publish have no match keys and will never be matched. |

---

## Greeting

When invoked, greet the consultant and orient them to the full journey:

```
Welcome to MDM Setup.

This skill guides you through an Informatica Cloud MDM deployment in three phases:

  PHASE 1 — Use Case Alignment
  We'll capture the business problem, identify the deployment pattern,
  and document the key decisions in a shareable workbook. You share it
  with stakeholders for review and sign-off before any technical work begins.

  PHASE 2 — Discovery Workbook
  Once the use case is approved, we translate it into specific technical
  configuration: source systems, data model extensions, survivorship rules,
  match model, data loading plan, and success criteria. The workbook is
  pre-populated with recommendations based on your use case — you review
  and fill any gaps.

  PHASE 3 — Deployment Coach
  The completed workbook drives a step-by-step deployment guide grounded
  in official Informatica documentation. Every irreversible action is
  flagged before you take it.
  Run: /mdm-deploy ~/Downloads/MDM_Discovery_{Client}.xlsx

Nothing is created in your org until Phase 3 is reviewed and confirmed.

Let's start with Phase 1. There are two ways in:

  PATH A — Template
  Start with a blank workbook and guided questions. Best when you are
  early in the engagement or do not yet have client documents.

  PATH B — Document Ingestion
  Provide client documents — system inventories, data dictionaries,
  compliance policies, sample data — and I will analyze them and
  pre-populate the workbook with confidence-coded recommendations.

Which path do you want to take?

  Note: To run in test mode (safe for org validation — prefixes all
  artifact names and org-written values with a test run ID), add --test:
    /mdm-setup --test
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

The workbook has 9 sheets. In template mode:
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

#### Sheet 3: `Data Model`

Header row (bold):
`Field Group Display Name` | `Field Group Internal ID` | `Source System` | `Field Display Name` | `Field Internal ID` | `Field Type` | `Notes`

Include 20 empty rows. Red-highlight the Field Group columns; yellow-highlight the Field columns.

Below the table, add a **guidance block** (light gray background):

```
FIELD GROUP RULES:
• Add one field group per source system that contributes aggregate fields
  not shared across all sources (e.g., account data from core banking,
  loan data from mortgage origination, portfolio data from wealth management)
• Use STATIC Field Group type — NOT Dynamic Field types
  Dynamic fields cannot have DQ rules or match rules applied to them
  Source: B360_April2026_DefineTheDataModel_en.pdf, p.18
• Supported field types: Text | Decimal | Integer | Date | Boolean
• Field group Internal IDs: lowercase, underscores, no reserved keywords
  (Message Type, _ingress, fieldGroup_State, sourcePKey, parentId are reserved)
• Field groups on predefined entities CAN be deleted
  Custom entities CANNOT be deleted — always extend c360.person, not a custom entity
  Source: B360_April2026_DefineTheDataModel_en.pdf, p.10
• Nested field groups supported up to 6 levels — use sparingly
• Reference: only fields in this sheet will be mapped in the CDI ingress (Step 6)

FIELD GROUP SOURCE PRIMARY KEY (FGID) — ANSWER BEFORE BUILDING SOURCE CSVs:
• Every field group used in File Import requires a Source Primary Key column in the CSV
  (e.g., address_fgid, phone_fgid, email_fgid). This is separate from the record's
  own Source Primary Key (client_id, borrower_id, etc.)
• The FGID uniquely identifies a field group instance WITHIN a source record —
  it does NOT need to be globally unique across all records
• DISCOVERY QUESTION (answer per field group per source system):
    How many instances of this field group does one source record have?
    — One instance (one address per person): FGID = 1 for all rows
    — Multiple instances (home + work + billing address): FGIDs must be
      unique within the record (1, 2, 3...); represent each instance as a
      separate CSV row with the same source primary key and different FGID values
• Document the cardinality answer here before creating source CSVs.
  Getting this wrong requires rebuilding the CSV and re-importing.
  Source: C360_April2026_Customer360SaaS_en.pdf, p.168, p.179
```

---

#### Sheet 4: `Survivorship`

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

#### Sheet 5: `DQ Planning`

**Purpose:** Capture the data quality decisions that drive Step 4 of the deployment. Every rule configured in Step 4 must be planned here first — type, function, severity, and trust impact grounded in profiling data from Sheet 9.

---

**Section A — Field-Level Rule Plan**

Header row (bold):
`Field` | `Field Group` | `Affected Sources` | `DQ Issue` | `Rule Type` | `Function / Spec` | `Severity` | `Trust Downgrade %` | `Notes`

Include 15 empty rows, yellow-highlighted.

Guidance block:
```
DQ ISSUE TYPES (fill from profiling data in Sheet 9):
  name_casing       — ALL CAPS or mixed case across sources → Title Case (Basic)
  address_abbrev    — "St" vs "Street" vs "St." variation → DaaS Address
  name_format       — "Smith, John" vs "John Smith" → DaaS Name (separate entitlement)
  phone_format      — format variation → Regular Match or DaaS Phone
  null_required     — null rate > 0% on a required field → Minimum Length validation
  invalid_pattern   — format does not match expected pattern → Regular Match (Basic)
  identifier_ssn    — SSN validation needed → DUNS SSN Validation (Advanced)
  concat_needed     — blank-canvas entity needs fullName from firstName+lastName → Concatenate with Spaces (Basic)

RULE TYPES:
  Basic    — predefined functions built into B360. No external dependency.
             Functions: Title Case, Trim, Concatenate with Spaces, Regular Match,
             Minimum/Maximum Length, Minimum/Maximum Value
  Advanced — Cloud Data Quality rule specification. Requires CDQ asset + entitlement.
             Use for: SSN/NPI/DUNS validation, custom identifier patterns
  DaaS     — Informatica Data-as-a-Service. Requires entitlement per service type.
             Address Verification: included in standard MDM SaaS license
             Name Standardization: SEPARATE entitlement — confirm before planning
             Email Verification: confirm with Informatica licensing
             Phone Verification: confirm with Informatica licensing

SEVERITY LEVELS:
  Information — rule runs; result recorded; record saves regardless of outcome
  Warning     — rule runs; trust score downgraded if fails; record saves
  Error       — rule runs; record REJECTED if fails; use with caution on ingress

TRUST DOWNGRADE %:
  How much to deduct from trust score when a field fails validation.
  Example: 20% downgrade on address validation failure means that source's
  address field loses 20 points — making a higher-ranked source more likely to win.
  This is the survivorship tie-in: bad data loses the trust contest automatically.
  Source: B360_April2026_ConfigureDataQuality_en.pdf, p.13
```

---

**Section B — DaaS Entitlement Check**

Pre-filled table (white background, review and confirm):

| DaaS Service | Entitlement | Action Required |
|---|---|---|
| Address Verification | Included in standard MDM SaaS license | Enable Address_Verifier_OOTB in Step 4 |
| Name Standardization | SEPARATE entitlement — not bundled | Confirm with Informatica licensing before planning |
| Email Verification | Confirm with Informatica licensing | Verify before planning |
| Phone Verification | Confirm with Informatica licensing | Verify before planning |

Guidance block:
```
Name standardization is the most commonly assumed-but-missing entitlement.
If your plan relies on DaaS Name Standardization and the entitlement is not
present, the rule will fail silently at ingress time.
Confirm entitlement BEFORE adding Name Standardization to Section A.
Alternative for name casing: use Basic → Title Case (no entitlement required).
```

---

**Section C — Blank-Canvas Prerequisites**

Pre-filled checklist (yellow — fill before Step 4):

| Prerequisite | Required when | Status |
|---|---|---|
| fullName Text field added to entity | Entity has separate firstName + lastName root fields (blank-canvas) | |
| Concat Full Name DQ rule configured | fullName field exists and match model uses Person_Name | |

Guidance block:
```
WHY FULLNAME IS REQUIRED (blank-canvas entities only):
  The match model's Person_Name field type expects a single combined name field.
  If your entity has firstName and lastName as separate root fields, you must:
    1. Add a fullName Text root field to the entity (Step 2)
    2. Configure a Basic DQ rule on fullName: Concatenate with Spaces
       Input 1: firstName | Input 2: lastName | Output: implicit (fullName)
  This rule must be configured BEFORE the match model is created (Step 5).
  Doc basis: MDM.md line 882-888
```

---

#### Sheet 6: `Match Model`

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

#### Sheet 7: `Data Loading`

**Section A — Loading Path Decision**

| Field | Cell color | Guidance |
|-------|-----------|---------|
| Loading path | Red | CDI (recommended — any volume, reusable, schedulable) / File Import (≤500 rows, smoke test or initial validation) |
| Decision reasoning | Yellow | Why this path was chosen |

Guidance block:
```
CDI vs. FILE IMPORT — CHOOSE BEFORE STEP 6:

  File Import
  • Best for: initial smoke test, ≤500 rows, no Secure Agent required
  • Limitations: cannot hardcode constants (e.g., Phone Type = "Mobile"),
    manual column additions (fgid) each schema change, not schedulable
  • Use for: demo validation, first-load verification

  CDI Ingress
  • Best for: production deployments, any volume, automated scheduling
  • Requires: Secure Agent, IDMC connection per source, CDI mapping per source
  • Advantages: hardcode constants in mapping, reusable, versioned, schedulable,
    handles field group mapping automatically via Business 360 Connector
  Source: C360_April2026_Customer360SaaS_en.pdf, p.179
```

---

**Section B — File Import Configuration** *(complete if File Import chosen)*

| Field | Cell color | Guidance |
|-------|-----------|---------|
| Intentional near-duplicates? | Yellow | Y/N — include pairs that should merge to validate M&M |
| Near-duplicate description | Yellow | Describe the pairs |

**fgid column plan** — complete per source system:

Header: `Source System` | `Field Group` | `Field Group Internal ID` | `fgid Column Name` | `Value Strategy`

Guidance block:
```
fgid COLUMN NAMING: {fieldGroupInternalId}_fgid  (camelCase internal ID of the group)
  Standard groups: address_fgid, phone_fgid, electronicAddress_fgid,
                   alternateName_fgid, identifier_fgid
  Custom groups:   {X_GroupInternalId}_fgid  (e.g., X_BankAccount_fgid)
  Value: "1" when each record has exactly one instance of the group
         Sequential (1, 2, 3...) when a record has multiple instances

DATE FIELDS — irreversible decision:
  Date type:     accepts yyyy-MM-dd (no time suffix)
  DateTime type: requires yyyy-MM-dd HH:mm:ss (append 00:00:00 to date-only values)
  This field type is set in the entity (Step 2) and cannot change after records exist.
  Confirmed per field: fill column "Date or DateTime?" in Sheet 3.
```

---

**Section C — CDI Ingress Configuration** *(complete if CDI chosen)*

**Runtime environment:**

| Field | Cell color | Guidance |
|-------|-----------|---------|
| Secure Agent group name | Red | Name of the runtime environment in IDMC Administrator |
| Agent status | Yellow | Confirm agent is Running before Step 6 |

**Per source system** — one block per source (repeat template):

Header: `Property` | `Value`

| Property | Guidance |
|---|---|
| Source system internal ID | From Sheet 2 — must match exactly |
| Connection type | Salesforce / Oracle / SQL Server / Snowflake / PostgreSQL / MySQL / Flat File / other |
| Connection name in IDMC | Existing connection name, or "new" if not yet created |
| Source object / table / query | Exact table name or SQL query |
| Primary key column | Column that maps to sourcePKey (no spaces, no / \ . % ; ") |
| Date fields | List each date column and whether it is Date or DateTime type in the entity |
| Constants needed | Fields the CDI mapping must hardcode (e.g., phoneType = "Mobile") |
| Field groups to map | From Sheet 3 — list groups this source contributes to |
| Mapping name | {sourceName}_to_{entityInternalId} |

Guidance block:
```
CDI MAPPING STRUCTURE (Business 360 Connector):
  Source transformation:
    Connection: {connection name}
    Object: {table or query from above}

  Target transformation:
    Connector: Business 360 Connector
    Business Entity: {entity internal ID}
    Source System: {source system internal ID from Sheet 2}
    Operation: Upsert

  Field mapping format for custom field groups:
    {fieldGroupInternalId}.{fieldInternalId}
    Example: X_Portfolio.portfolioId

  sourcePKey rules:
    No spaces, no / \ . % ; " characters
    Test mode: prefix TEST_{NNN}_

  Constants (hardcode in mapping — not possible in File Import):
    Add an Expression transformation between Source and Target
    Output a constant string for fields the source does not provide
    (e.g., phoneType = "Mobile", addressType = "Home")

  Connection setup (if connection does not exist):
    IDMC → Administration → Connections → New Connection
    Select connection type → provide credentials → Test → Save
    Secure Agent must be Running before connection can be tested

  Mapping publication:
    Save mapping → click Publish to activate
    A mapping must be Published before the ingress job in Step 7 can run it

Source: B360_April2026_Business360Connector_en.pdf
```

---

**Section D — Field Mapping Reference** *(pre-filled, white)*

Standard entity root fields:

| Field Display Name | Internal ID | Type | CDI Target Path |
|---|---|---|---|
| First Name | firstName | Text | firstName |
| Middle Name | middleName | Text | middleName |
| Last Name | lastName | Text | lastName |
| Full Name | fullName | Text | fullName |
| Birth Date | birthDate | DateTime | birthDate |

Custom field groups — format reminder:
```
{fieldGroupInternalId}.{fieldInternalId}
Source Primary Key column maps to: {fieldGroupInternalId}.sourcePKey
```

---

#### Sheet 8: `Success Criteria`

Pre-filled checklist (white, review and confirm):

| Step | What to verify | How to verify | Confirmed? |
|------|---------------|---------------|------------|
| Step 1 — Source Systems | All source systems present with correct Internal IDs | Business 360 Console → Source Systems | |
| Step 2 — Data Model | All field groups visible on c360.person canvas | Business 360 Console → Explore → c360.person | |
| Step 3 — Survivorship | Source ranking and decay rules saved | c360.person → Survivorship tab | |
| Step 4 — Data Quality | Rule associations visible on Data Quality tab | c360.person → Data Quality tab | |
| Step 5 — Match Model | person.ruleset1 status = Published | c360.person → Match tab | |
| Step 6 — CDI Ingress | All source mappings Published in IDMC | IDMC → Data Integration → Mappings | |
| Step 7 — Ingress Job | All source ingress jobs show Succeeded | IDMC → My Jobs + mdm_scan_org.py record count | |
| Step 8 — M&M Trigger | M&M job completed with SUCCESS | mdm_trigger_match_merge.py output | |
| Step 9 — Golden Records | Golden records exist, near-duplicate pairs consolidated, aggregate fields populated | mdm_verify_records.py output | |

**Use case validation row** (yellow — fill based on use case):

| Use Case Validation | What correct looks like for THIS deployment | Verified? |
|----|----|----|
| [fill from Use Case sheet] | [describe expected outcome] | |

---

#### Sheet 9: `Profiling Results`

**Purpose:** Capture IDMC Data Profiling task results for each source system before finalizing Sheets 4 (Survivorship) and DQ configuration. This sheet grounds survivorship ranking and DQ rule selection in measured data quality, not assumptions.

**When to populate:** After generating this workbook, run a Data Profiling task in IDMC against each source object (one task per source system). Export results (Actions → Export) and fill this sheet. Then revisit Sheet 4 (Survivorship) and confirm rankings reflect completeness scores.

One section per source system. Header row (bold):
`Column` | `Declared Type` | `Row Count` | `Null Count` | `Null %` | `Distinct Count` | `Distinct %` | `Pattern Count` | `Top Pattern` | `Top Pattern %` | `Notes / DQ Issues`

Color coding:
- **Red** — Null % > 10% or Pattern Count > 2 (format inconsistency flag)
- **Yellow** — Null % 1–10% or Pattern Count = 2
- **White** — clean (Null % = 0, single pattern)

Below each source section, add a **DQ Summary** row:
```
Overall Completeness:  {%}
Format Issues:         {list affected columns}
Survivorship Signal:   {based on completeness — recommended rank and why}
DQ Rules Indicated:    {list rule type → field, grounded in profiling data}
```

Guidance block (light gray):
```
PROFILING → SURVIVORSHIP LINK:
  Higher completeness score = higher trust rank.
  More format patterns on a field = stronger case for a DQ standardization rule.
  Compare null rates across sources for shared fields — the source with lower
  null rate on name/address/phone should rank higher for those fields.

PROFILING → DQ RULES LINK:
  Pattern Count > 1 on phone/zip/date → standardization rule needed
  Null % > 0 on required fields → completeness validation rule
  Inferred type ≠ declared type → format validation rule
  Name casing variation (ALL CAPS rows) → Title Case Basic rule
  Embedded middle initial in FIRST_NAME → Advanced Name Parser rule spec

PROFILING API (alternative to UI export):
  Base: https://{pod}-dqprofile.dm-{region}.informaticacloud.com/profiling-service/api/v1/
  Auth: POST https://dm-{region}.informaticacloud.com/ma/api/v2/user/login → IDS-SESSION-ID
  List profiles: GET /profile/
  Profile detail: GET /profile/{id}
  Script: mdm_fetch_profile_results.py (see scripts/)
```

---

### A3 — Phase 1 complete — deliver Use Case workbook

```
✓ Phase 1 complete.

We've captured the business context for {Client}, identified the deployment
pattern ({pattern name}), and documented all key decisions and open questions.

What was produced:
  MDM_UseCase_{Client}.xlsx  →  ~/Downloads/

What to do next:
  1. Open the workbook and review each section
  2. Share it with stakeholders, peers, or the client for alignment
  3. Resolve the open questions in Section 5 before proceeding
  4. Once approved, run:

       /mdm-setup confirm ~/Downloads/MDM_UseCase_{Client}.xlsx

     This will:
       • Lock the approved use case as a PDF (the official record)
       • Open Phase 2 — the Discovery Workbook with technical configuration

Nothing in your org has been touched. Phase 2 does not start until you confirm.
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
- Source-specific data domains → Data Model field group candidates (Sheet 3)

#### Data dictionary / schema (Excel, CSV, PDF)
Extract:
- Field names and data types → Sheet 7 field mapping
- Fields unique to one source system → Data Model field group candidates (Sheet 3)
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
- Known data quality issues → DQ rule candidates + verification criteria additions

---

### B3 — Print extraction summary

```
Signals extracted from {N} documents:

  Source systems identified:     N  ({list names})
  Field mappings extracted:      N columns across N tables
  Source-specific field groups:  N candidates → Sheet 3
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

Generate the same 9-sheet workbook as Path A, but pre-populated:

- **White** — high confidence, inferred from documents (cite which doc)
- **Yellow** — recommendation from pattern knowledge, needs consultant review
- **Red** — required, could not be inferred — must be filled before resuming
- **Light gray** — guidance text (same as template)

For every pre-filled recommendation, include the source in the cell note:
> "Recommended based on [doc name] — [one sentence reasoning]"

---

### B6 — Phase 1 complete — deliver populated Use Case workbook

```
✓ Phase 1 complete.

I've analyzed {N} documents and extracted signals covering {N} source systems,
{N} field mappings, and {N} regulatory drivers. The deployment pattern was
identified as {pattern name} ({confidence} confidence).

What was produced:
  MDM_UseCase_{Client}.xlsx  →  ~/Downloads/
  (pre-populated from your documents — confidence-coded)

  White cells  — high confidence, ready to confirm
  Yellow cells — recommended, needs your review
  Red cells    — {N} required fields that could not be inferred

Key items needing your review before sharing:
  [list 3-5 most important yellow/red cells]

What to do next:
  1. Review and fill any RED cells
  2. Share the workbook with stakeholders for alignment and sign-off
  3. Once approved, run:

       /mdm-setup confirm ~/Downloads/MDM_UseCase_{Client}.xlsx

     This will:
       • Lock the approved use case as a PDF (the official record)
       • Open Phase 2 — Discovery Workbook with technical configuration

Nothing in your org has been touched. Phase 2 does not start until you confirm.
```

---

## CONFIRM — Lock Use Case and Open Phase 2

Invoked as: `/mdm-setup confirm <path/to/MDM_UseCase_<Client>.xlsx>`

### C1 — Narrate the transition

```
✓ Use Case confirmed.

Phase 1 is now locked. Here is what was approved:

  Client:             {Client}
  Deployment pattern: {pattern}
  Source systems:     {list}
  Trust ranking:      {ranking}
  Match strategy:     {strategy}
  Open items:         All resolved

What happens now:
  1. Generating MDM_UseCase_{Client}.pdf — the locked, official record of
     what was agreed before any technical work begins.

  2. Opening Phase 2 — Discovery Workbook.

     Phase 2 translates the approved use case into specific technical
     configuration for your org: source system IDs, data model extensions,
     survivorship rules, match model settings, data loading plan, and
     success criteria.

     The workbook is pre-populated with your approved decisions. You will
     review, fill any remaining gaps, and confirm before deployment begins.

     Nothing in your org is touched in Phase 2 — this is still planning.
```

### C2 — Generate the approved PDF

Using `reportlab`, produce a clean formatted PDF from the confirmed Use Case workbook. The PDF includes:
- All confirmed decisions from Sections 1–3
- Open Items section relabeled as "Resolved" with resolutions filled in
- Green "APPROVED — Locked for Technical Planning" banner
- Sign-off section with approver names
- Footer: "This document is locked. To revise, re-run /mdm-setup."

Save as `MDM_UseCase_{Client}_APPROVED.pdf` in the same directory as the xlsx.

### C3 — Generate the Discovery Workbook

Generate `MDM_Discovery_{Client}.xlsx` — the 9-sheet workbook, pre-populated from the confirmed Use Case decisions. Green cells carry forward confirmed values. Yellow cells remain for the consultant to review. Red cells are remaining required fields. Sheet 9 (Profiling Results) is empty — it must be populated from IDMC profiling task exports before the workbook is considered complete.

Print:
```
✓ Locked: MDM_UseCase_{Client}_APPROVED.pdf

✓ Phase 2 opened: MDM_Discovery_{Client}.xlsx
  9 sheets — Use Case, Source Systems, Data Model, Survivorship,
              DQ Planning, Match Model, Data Loading, Success Criteria, Profiling Results

  GREEN cells  — pre-filled from your approved use case
  YELLOW cells — review recommended before running the plan
  RED cells    — {N} required fields still needed

─── REQUIRED BEFORE RESUMING — Run Data Profiling ────────────────

  Sheet 9 (Profiling Results) must be populated before you run
  /mdm-deploy. Profiling results ground your survivorship
  ranking (Sheet 4) and DQ rule selection (Step 4) in measured
  data quality, not assumptions.

  Steps:
    1. In IDMC → Data Integration → New → Data Profiling Task
    2. Create one task per source system, pointing at each source table
    3. Run each task → wait for Succeeded in My Jobs
    4. Actions → Export → save the Excel file
    5. Paste key metrics into Sheet 9 (Profiling Results)
    6. Revisit Sheet 4 — confirm survivorship ranking reflects
       the completeness scores from profiling

  Alternative: use mdm_fetch_profile_results.py to pull results
  via the Data Profiling REST API (see scripts/).

──────────────────────────────────────────────────────────────────

Complete the workbook and profiling, then run:
  /mdm-deploy ~/Downloads/MDM_Discovery_{Client}.xlsx
```

