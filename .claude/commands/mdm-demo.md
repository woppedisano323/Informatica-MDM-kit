---
description: Narrated demo of the Informatica MDM Kit — walks through the full three-skill chain using PROFILE-TEST-001 FSI scenario data. No live IDMC session required. Runs in 15–20 minutes. Designed for peer review, client demos, and conference use. Invoked as /mdm-demo
---

# MDM Kit — Demo Walkthrough

You are presenting the Informatica MDM Kit to an audience of SAs, Consultants, or a client. This demo walks through the full three-skill chain using the PROFILE-TEST-001 FSI scenario — a pre-built example with three real source files, actual profiling results, and a verified golden record outcome.

No live IDMC session is required. All data comes from `examples/PROFILE-TEST-001/`.

**Format:** Narrated storytelling, not interactive coaching. Present each scene, show the actual numbers, pause for questions, then advance.

**Pace:** One scene at a time. After each scene, ask "Ready for the next scene?" unless the audience signals to continue.

---

## Demo Inventory

Pre-loaded artifacts in `examples/PROFILE-TEST-001/`:

| File | Contents |
|------|----------|
| `MDM-PROFILE-TEST-001-20261027_ORION_CLIENTS_DIRTY.csv` | 100 rows — wealth management source |
| `MDM-PROFILE-TEST-001-20261027_ENCOMPASS_LOAN_CUSTOMERS_DIRTY.csv` | 100 rows — loan origination source |
| `MDM-PROFILE-TEST-001-20261027_FISERVER_CUSTOMERS_DIRTY.csv` | 100 rows — core banking source |
| `MDM_Discovery_FSI.xlsx` | Completed 9-sheet Discovery Workbook |
| `MDM_Profile_DQ_FSI.xlsx` | Populated 7-sheet Profile/DQ Workbook |

---

## Narration Guide

### SCENE 1 — The Scenario

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE 1 — The Scenario
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A mid-size FSI firm runs three separate platforms:
  • ORION Wealth Management   — investment accounts and advisor assignments
  • ENCOMPASS Loan Origination — mortgage and loan records
  • FiServ Core Banking        — savings, checking, and money market accounts

The same person is in all three systems with no shared key.
Nobody knows if ORION client "JAMES MORRISON" is the same person
as ENCOMPASS borrower "James Morrison" and FiServ account holder
"James Morrison" — they think it is, but they have no proof.

Business problem:
  "We cannot run cross-sell or retention campaigns because we do
   not know which products each customer already has."

The ask: Unified Customer 360 in Informatica MDM SaaS.

────────────────────────────────────────────────────────────────
This is the starting point for the kit. Let's walk through what
happens from here.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### SCENE 2 — What /mdm-setup Produced

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE 2 — /mdm-setup: From Questions to Blueprint
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/mdm-setup asked 9 sheets of questions. Here is what it decided:

DEPLOYMENT PATTERN
  Customer 360 / Unified View
  Rationale: three systems, identity match needed, one golden record

ENTITY DESIGN
  ✓ Blank-canvas Business Entity — NOT a copy of c360.person
  Why: Person copy inherits smart fields with DQ associations that
       require dictionary privileges not in standard B360 roles.
       Copying Person causes silent load failures on all Picklist fields.
  The kit enforces the blank-canvas path and explains why.

DATA MODEL (Sheet 3)
  8 field groups · 28 custom fields
  Identity    → first_name, last_name, birth_date, ssn_last4
  Contact     → phone, email, street_address, city, state, postal_code
  ORION       → portfolio_id, portfolio_tier, risk_rating, advisor_id
  ENCOMPASS   → loan_number, loan_type, loan_amount, loan_status
  FiServ      → account_number, account_type, credit_tier, branch_id
  Metadata    → created_date, updated_date, source_system

SOURCE SYSTEMS (Sheet 2)
  ORION_WEALTH_MGMT  (internal ID — permanent after creation)
  ENCOMPASS_LOAN     (internal ID — permanent after creation)
  FISERVER_CORE      (internal ID — permanent after creation)

  ⚠️  Internal IDs are immutable — if you create ORION_WEALTH_MG by
      mistake and need ORION_WEALTH_MGMT, you must delete and recreate
      the source system. The skill warns before you type this value.

SURVIVORSHIP (Sheet 4 — draft, pending profiling)
  Initial ranking: ORION #1, ENCOMPASS #2, FISERVER #3
  (based on assumed record completeness — before profiling)
  We will update this after Scene 5.

DQ PLANNING (Sheet 5 — draft, pending profiling)
  11 DQ issues flagged as "pending profiling evidence"
  Rule types: Basic, Advanced, DaaS Address Verification
  We will populate the evidence in Scene 6.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Open MDM_Discovery_FSI.xlsx to show the workbook live.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### SCENE 3 — Why Profile Before Deploying

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE 3 — The Step We Always Skip
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Most MDM engagements go straight from discovery to deployment.
What gets missed:

  "Which source should be Rank 1 for survivorship?"
  → Usually a gut call or politics.
  → We just assumed ORION because it has the most fields.
  → After profiling: ORION has 3 phone formats, ALL-CAPS names,
    and 3 state variants. It is NOT Rank 1.

  "What DQ rules do we need?"
  → Usually guesswork until the load fails.
  → CDI expression transforms get added reactively when the data
    lands wrong.

  "Will match rule 3 (email + phone) actually fire?"
  → Only if email and phone are both non-null.
  → FISERVER has 13% null email. 13 of 100 records will never
    be matched by that rule — but we would not know that until
    after deployment.

/mdm-profile changes the decision sequence:
  Profile first → evidence-backed DQ rules → CDI transforms
  before load → survivorship ranking based on data quality,
  not assumption.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### SCENE 4 — Profiling Results: ORION

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE 4 — IDMC Profiling Results: ORION Wealth Management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source file: ORION_CLIENTS_DIRTY.csv  (100 rows · 16 fields)

Field             Null%   Patterns  Top Pat%  Flag
─────────────────────────────────────────────────────────────────
first_name        0%      7         29%       🔴   ALL CAPS subset (~27%)
last_name         0%      6         31%       🔴   ALL CAPS subset
phone             0%      3         42%       🔴   3 formats: plain/dots/dashes
state             0%      3         67%       🔴   CA / ca / California
postal_code       0%      2         81%       🟡   5-digit + 5+4 mix (19%)
birth_date        0%      1         100%      ✅   YYYY-MM-DD — clean
email             0%      —         —         ✅   0% null — all records matchable
client_id         0%      1         100%      ✅   100% distinct — no duplicates

KEY FINDINGS:
  • Phone needs REG_REPLACE to strip separators before MDM stores it
  • Names need INITCAP — ALL CAPS will break text search in B360
  • State variants need normalization — 3 values for the same field
    will create 3 separate facets in the golden record UI
  • Postal 5+4 needs SUBSTR to strip +4 suffix

DATA TYPE WARNINGS:
  • birth_date: IDMC infers Date(year/dd/mm) — this is a FALSE POSITIVE
    on clean YYYY-MM-DD data where month ≤ 12. Raw data confirmed
    YYYY-MM-DD — no transformation needed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Open MDM_Profile_DQ_FSI.xlsx → "Source 3 — ORION" tab.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### SCENE 5 — Profiling Results: ENCOMPASS

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE 5 — IDMC Profiling Results: ENCOMPASS Loan Origination
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source file: ENCOMPASS_LOAN_CUSTOMERS_DIRTY.csv  (100 rows · 17 fields)

Field             Null%   Patterns  Top Pat%  Flag
─────────────────────────────────────────────────────────────────
first_name        0%      5         38%       🟡   Mixed casing — INITCAP needed
last_name         0%      4         41%       🟡   Mixed casing
phone             15%     3         52%       🔴   15% null + 3 formats (parens/dashes/plain)
birth_date        0%      2         54%       🔴   2 formats: MM/DD/YYYY (46%) + YYYY-MM-DD (54%)
email             0%      —         —         ✅   0% null
state             0%      1         100%      ✅   All 2-char abbreviations
zip_code          0%      1         100%      ✅   All 5-digit

KEY FINDINGS:
  • birth_date has TWO formats in the same column — IIF logic needed
    in CDI to detect and convert both:
    IIF(INSTR(birth_date,'/')>0, TO_DATE(birth_date,'MM/DD/YYYY'),
                                 TO_DATE(birth_date,'YYYY-MM-DD'))
  • 15% null phone means match rule 3 (email + phone) will not
    fire for 15 records. These will match on name + DOB only.
    Important: without profiling, this gap would be invisible
    until post-load match rate analysis.
  • Names are Title Case — INITCAP is still recommended because
    mixed source data will land mixed in the golden record if
    not normalized at load time.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Open MDM_Profile_DQ_FSI.xlsx → "Source 2 — ENCOMPASS" tab.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### SCENE 6 — Profiling Results: FiServ

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE 6 — IDMC Profiling Results: FiServ Core Banking
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source file: FISERVER_CUSTOMERS_DIRTY.csv  (100 rows · 15 fields)

Field             Null%   Patterns  Top Pat%  Flag
─────────────────────────────────────────────────────────────────
first_name        0%      5         42%       🟡   Mixed casing — INITCAP needed
last_name         0%      6         35%       🔴   ALL CAPS subset
phone             0%      4         38%       🔴   4 patterns detected
                                                    ⚠️ Data type: INTEGER (all-digit)
email             13%     —         —         🟡   13% null — affects match rule 3
birth_date        0%      2         87%       🟡   YYYY-MM-DD (87%) + outlier (13%)
state             0%      1         100%      ✅   All 2-char
zip_code          0%      1         100%      ✅   All 5-digit

KEY FINDINGS:
  • Phone field was stored without separators — IDMC inferred INTEGER
    not String. This is a known IDMC profiling issue.
    CDI fix: TO_CHAR(phone) wraps before REG_REPLACE:
    REG_REPLACE(TO_CHAR(phone), '[^0-9]', '')
    (This is documented in the Known Issues section of /mdm-profile)

  • 13% null email: 13 records will only match on name + DOB
    (or phone if available). Match rule 3 will not fire for these.
    Recommendation: note null % in survivorship rationale — FiServ
    is still Rank 1 on other completeness metrics.

  • birth_date outlier format (13%): check raw data to identify
    the format before writing the IIF expression.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Open MDM_Profile_DQ_FSI.xlsx → "Source 1 — FISERVER" tab.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### SCENE 7 — DQ Analysis: 11 Rules

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE 7 — DQ Analysis: 11 Rules, Evidence-Backed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Before profiling: "we need DQ rules but we are not sure which ones"
After profiling: 11 specific rules with rationale and trust impact

RULE  FIELD         ISSUE                   TYPE      SEV      TRUST △%
────────────────────────────────────────────────────────────────────────
R01   first_name    Casing normalization    Basic     Warning    5%
R02   last_name     Casing normalization    Basic     Warning    5%
R03   phone         Format normalization    Basic     Warning    8%
R04   phone         Null on required field  Basic     Warning   12%  (ENCOMPASS only)
R05   email         Null on match field     Basic     Warning   10%  (FISERVER only)
R06   birth_date    Mixed date formats      Advanced  Warning    5%
R07   state         Variant normalization   Basic     Warning    5%
R08   postal_code   5+4 suffix present      Basic     Info       0%
R09   address       DaaS Address Verify     DaaS      Warning   10%
R10   sourcePKey    Null primary key        Basic     Error     N/A  (reject record)
R11   first_name    Null on identity field  Basic     Error     N/A  (reject record)

RULE TYPES USED:
  Basic (R01-R08, R10-R11) — MDM predefined functions in B360 entity settings
  Advanced (R06) — Cloud DQ rule spec for multi-format date handling
  DaaS (R09) — Address Verification (included in MDM SaaS, must be enabled)

⚠️  R04, R05 are source-specific rules — apply only to ENCOMPASS and FISERVER
    respectively. Not every rule applies to every source.

⚠️  DaaS Phone/Email Verification (not listed here) — requires separate
    entitlement. Confirmed not in scope for this engagement.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Open MDM_Profile_DQ_FSI.xlsx → "DQ Analysis" tab.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### SCENE 8 — CDI Transformation Plan

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE 8 — CDI Transformations: Fix at Load Time
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

These go into the Expression transformation in the CDI mapping canvas
before the Business 360 Connector target.

─── ORION ──────────────────────────────────────────────────────
first_name   INITCAP(first_name)
last_name    INITCAP(last_name)
phone        REG_REPLACE(phone, '[^0-9]', '')
state        IIF(LENGTH(UPPER(state))>2,
               IIF(UPPER(state)='CALIFORNIA','CA',UPPER(state)),
               UPPER(state))
postal_code  SUBSTR(postal_code, 1, 5)

─── ENCOMPASS ──────────────────────────────────────────────────
first_name   INITCAP(first_name)
last_name    INITCAP(last_name)
phone        IIF(ISNULL(phone) OR phone='', NULL,
               REG_REPLACE(phone, '[^0-9]', ''))
birth_date   IIF(INSTR(birth_date,'/')>0,
               TO_DATE(birth_date,'MM/DD/YYYY'),
               TO_DATE(birth_date,'YYYY-MM-DD'))

─── FISERVER ───────────────────────────────────────────────────
first_name   INITCAP(first_name)
last_name    INITCAP(last_name)
phone        IIF(ISNULL(phone), NULL,
               REG_REPLACE(TO_CHAR(phone), '[^0-9]', ''))
             ← TO_CHAR wraps because IDMC inferred INTEGER
email        IIF(ISNULL(email) OR email='', NULL, email)

KEY DESIGN POINT:
  One Expression transformation per source mapping handles all
  field-level transforms. No separate transformations per field.
  Three CDI mappings total (one per source) → Business 360 Connector.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Open MDM_Profile_DQ_FSI.xlsx → "CDI Transformations" tab.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### SCENE 9 — Survivorship Ranking (Updated)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE 9 — Survivorship: Before and After Profiling
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEFORE PROFILING (gut call):
  Rank 1: ORION         "biggest wealth management system, most fields"
  Rank 2: ENCOMPASS     "loan data is usually clean"
  Rank 3: FISERVER      "older core banking platform"

AFTER PROFILING (evidence-backed):
  Rank 1: FISERVER      Rank 2: ENCOMPASS     Rank 3: ORION

FISERVER #1 — Why:
  ✓ 100% phone completeness (all records have phone)
  ✓ 0% null on identity fields (first_name, last_name, birth_date)
  ✓ Single state format (all 2-char abbreviations)
  ✓ 87% single birth_date format — most consistent date data
  Note: 13% null email accepted — email is secondary match, not
  primary identity field

ENCOMPASS #2 — Why:
  ✓ 0% null email — strong secondary match coverage
  ✓ Clean state (100% 2-char) and postal (100% 5-digit)
  △ 15% null phone — significant gap, noted in trust decay
  △ Mixed birth_date formats require IIF transform

ORION #3 — Why:
  △ 3 phone formats — lowest format consistency
  △ 3 state variants — normalization required
  △ ALL CAPS names in ~27% of records
  △ 5+4 postal in 19% of records
  Lowest data quality on key match/identity fields

SURVIVORSHIP IMPACT:
  When sources disagree on a field value, the Rank 1 source wins.
  James Morrison's phone:
    ORION:     9513456789 (raw — pre-transform: plain digits)
    ENCOMPASS: (951) 345-6789 → 9513456789 after REG_REPLACE
    FISERVER:  951-345-6789 → 9513456789 after TO_CHAR+REG_REPLACE
  All three resolve to 9513456789 — survivorship agrees, trust is additive.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Open MDM_Profile_DQ_FSI.xlsx → "Summary" tab.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### SCENE 10 — Deployment: Key Moments

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE 10 — /mdm-deploy: The Steps That Matter
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/mdm-deploy reads MDM_Discovery_FSI.xlsx, runs a pre-flight org
scan, then walks through 9 steps — one action at a time.

Key moments from this run:

STEP 1 — Source Systems
  Created three source systems with permanent internal IDs:
    ORION_WEALTH_MGMT · ENCOMPASS_LOAN · FISERVER_CORE
  ⚠️  Permanent warning was shown before each ID was typed.
      These cannot be changed after creation.

STEP 3 — Survivorship (before any records load)
  Configured ranking: FISERVER_CORE #1 · ENCOMPASS_LOAN #2
                      ORION_WEALTH_MGMT #3
  Added decay rules for account_open_date (max score logic)
  ⚠️  Survivorship must be configured before records exist.
      Trust scores are not retroactively recalculated.

STEP 4 — DQ Rules
  Configured 11 rules via EVO (Enrichment + Validation Orchestrator)
  Address DaaS enabled on the blank-canvas entity
  ⚠️  Phone/Email DaaS not enabled — separate entitlement required,
      confirmed out of scope in /mdm-setup

STEP 5 — Match Model
  Published person.ruleset1 (no customization needed for this use case)
  ⚠️  Match model must be Published before records load.
      Records loaded before publish have no match keys.

STEPS 6 + 7 — CDI Ingress
  3 CDI mappings built, Expression transforms applied per scene 8
  Ran all three ingress jobs:
    ORION:    100 rows loaded
    ENCOMPASS: 100 rows loaded
    FISERVER:  100 rows loaded

STEP 8 — Match and Merge
  Ran FISERVER_CUST360_MergeJob
  300 source records in → 17 golden records

STEP 9 — Validate
  32 customers appeared in all 3 sources (16 additional customers
  existed in only 1-2 sources → remained as unique golden records)
  Net: 300 source records → 17 golden records (15 merge events,
       17 distinct customers confirmed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### SCENE 11 — The Golden Record

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE 11 — The Result: James Morrison
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Three source records. Three different representations. One person.

BEFORE (three disconnected records):
  ┌─ ORION ORION_001 ───────────────────────────────────────────┐
  │  JAMES MORRISON · phone: 9513456789 · state: CA             │
  │  Portfolio: PORT-81482 · Risk: Medium · Advisor: ADV-132    │
  └──────────────────────────────────────────────────────────────┘
  ┌─ ENCOMPASS ENCO_001 ────────────────────────────────────────┐
  │  James Morrison · phone: (951) 345-6789 · DOB: 03/15/1968  │
  │  Loan: LN-862569 · Conventional · $877,886                 │
  └──────────────────────────────────────────────────────────────┘
  ┌─ FISERVER FSV_001 ──────────────────────────────────────────┐
  │  James Morrison · phone: 951-345-6789 · DOB: 1968-03-15    │
  │  Account: ACT-7219396 · Money Market · Private Banking      │
  └──────────────────────────────────────────────────────────────┘

AFTER (one golden record with three contributions):
  ┌─ GOLDEN RECORD ─────────────────────────────────────────────┐
  │  James Morrison                                              │
  │  DOB: 1968-03-15 · Phone: 9513456789                        │
  │  Email: james.morrison@email.com                             │
  │  Address: 142 Oak St, Riverside, CA 92501                   │
  │                                                              │
  │  Source Contributions:                                       │
  │    ✓ FISERVER_CORE   (Rank 1 · Trust: highest)              │
  │    ✓ ENCOMPASS_LOAN  (Rank 2)                                │
  │    ✓ ORION_WEALTH_MGMT (Rank 3)                             │
  │                                                              │
  │  Products:                                                   │
  │    Portfolio: PORT-81482 (Conservative · Medium)            │
  │    Loan: LN-862569 (Conventional · $877K · In Process)      │
  │    Account: ACT-7219396 (Money Market · Private Banking)    │
  └──────────────────────────────────────────────────────────────┘

The FSI firm now knows:
  • James Morrison is a Private Banking client with a wealth
    portfolio, an active mortgage, and a Money Market account
  • Cross-sell target: loan paydown advisory or estate planning
  • Retention flag: Conventional loan at 6.07% — refi candidate
    in current rate environment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is what the kit produces. End of demo.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Facilitator Notes

**Where to pause for questions:**
- After Scene 3 (the survivorship ranking flip is the "aha" moment)
- After Scene 7 (DQ rules with trust downgrade %)
- After Scene 11 (open floor before wrapping)

**If asked about live demo vs. narrated demo:**
```
This is a pre-loaded walkthrough using real IDMC profiling exports
and real CDI configuration. The actual /mdm-setup, /mdm-profile,
and /mdm-deploy skills are fully interactive — each one coaches
you through the real org in real time, one action at a time.

Clone the repo, open in Claude Code, run /mdm-setup to see the
interactive version.
```

**If asked "does this work on non-FSI use cases?":**
```
The three-skill chain works for any MDM SaaS deployment pattern.
The FSI scenario is the reference example — the kit supports
five deployment patterns: Customer 360, Marketing Dedup, KYC/AML,
Post-M&A Consolidation, and Data Migration Hub.

The profiling heuristics in /mdm-profile are domain-agnostic —
phone format normalization, date standardization, and casing
normalization apply to any customer dataset.
```

**If asked about effort / timeline:**
```
/mdm-setup:  45–90 minutes (first run; faster with a populated client brief)
/mdm-profile: 30–60 minutes (includes actual IDMC profiling runtime)
/mdm-deploy:  2–4 hours (depends on complexity of DQ rules and CDI mappings)

Demo-ready environment using examples/PROFILE-TEST-001/:
  30 minutes from clone to golden record with a pre-built org.
```

---

## Quick Reference — Artifacts

| Artifact | Generated by | When to open |
|----------|-------------|--------------|
| `MDM_UseCase_<Client>.xlsx` | /mdm-setup Phase 1 | Scene 2 — use case |
| `MDM_Discovery_<Client>.xlsx` | /mdm-setup Phase 2 | Scene 2 — technical blueprint |
| `MDM_Profile_DQ_<Client>.xlsx` | /mdm-profile | Scenes 4–9 |
| `MDM_Deployment_Steps_<Client>.xlsx` | /mdm-deploy | Scene 10 |
| Session PDF | /mdm-deploy (each step signoff) | Scene 10 — audit trail |
