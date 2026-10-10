# Informatica MDM Kit

Guided deployment skill for Informatica Cloud MDM — Business 360 / Customer 360 SaaS.

## Skill

### `/mdm-setup`

Produces a structured deployment plan for a new MDM org. The skill:

1. Captures the business use case and maps it to a known deployment pattern
2. Translates the use case into specific, justified technical decisions (source ranking, survivorship, match strategy)
3. Runs a read-only org scan to confirm current state before writing the plan
4. Produces `MDM_Deployment_Plan_<Client>.md` with every irreversible action flagged prominently before its step

Nothing is created in the org until the consultant reviews and confirms the plan.

## Scripts (in `scripts/`)

| Script | Purpose |
|--------|---------|
| `mdm_scan_org.py` | Read-only org scan — entity status, match model, source systems, record count, job definitions |
| `mdm_seed_records.py` | Seed c360.person records via Business Entity REST API (≤ 50 records) |
| `mdm_trigger_match_merge.py` | Trigger a Match & Merge job and poll to completion |
| `mdm_verify_records.py` | Verify golden records — consolidation status and source record contributions |

## Supported deployment patterns

| Pattern | Use case |
|---------|---------|
| Customer 360 / Unified View | One view of the customer across CRM, support, and engagement systems |
| Marketing Deduplication | Clean customer lists before campaigns; dedup across email, CRM, and ad platforms |
| Compliance / KYC / AML | Verified customer identity linked by regulatory identifiers |
| Post-M&A Consolidation | Merge customer records from two companies after acquisition |
| Data Migration Hub | Cleansing layer before cutover to a new platform |

## Documentation basis

All recommendations in generated plans cite official Informatica documentation:

- B360 April 2026: DefineSourceSystems, DefineJobs, ConfigureSurvivorship, ConfigureMatchAndMerge, DefineTheDataModel, REST API Reference, PredefinedAssets
- Informatica MDM Customer 360 SaaS Best Practices Guide (Aug 2024)
- B360 Workshop Lab Guide (Jun 2025)

## Usage

Open this repo in Claude Code. Then:

```
/mdm-setup
```

Claude will walk through use case discovery, technical intake, org scan, and plan generation.

## Prerequisites

- Informatica Cloud MDM org with Customer 360 SaaS provisioned
- c360.person entity available (predefined in every Customer 360 org)
- Python 3 (standard library only — no pip install required)
- IDMC username and password
