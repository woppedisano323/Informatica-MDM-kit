"""
mdm_overview_pdf.py — Generate the MDM Kit Skill Overview PDF.

Usage:
    python3 mdm_overview_pdf.py [output_path]

Default output: ~/Downloads/MDM_Setup_Skill_Overview.pdf
"""

import os
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

SF_NAVY     = colors.HexColor("#032D60")
SF_BLUE     = colors.HexColor("#0070D2")
SF_LBLUE    = colors.HexColor("#D9F0FC")
SF_GREEN    = colors.HexColor("#2E7D32")
SF_GREEN_BG = colors.HexColor("#E8F5E9")
SF_AMBER    = colors.HexColor("#F57C00")
SF_AMBER_BG = colors.HexColor("#FFF3E0")
SF_GREY_BG  = colors.HexColor("#F5F5F5")
SF_RED      = colors.HexColor("#C62828")
SF_RED_BG   = colors.HexColor("#FFEBEE")
WHITE       = colors.white
RULE_COLOR  = colors.HexColor("#E0E0E0")
NOTE_COLOR  = colors.HexColor("#555555")


def ps(name, **kw):
    d = dict(fontSize=8, fontName="Helvetica", textColor=colors.black, leading=11)
    d.update(kw)
    return ParagraphStyle(name, **d)


BODY  = ps("body", fontSize=8, leading=11)
SMALL = ps("small", fontSize=7, leading=10, textColor=NOTE_COLOR, fontName="Helvetica-Oblique")
SEC_H = ps("sech", fontSize=10, fontName="Helvetica-Bold", textColor=SF_NAVY, spaceAfter=3, spaceBefore=10)
H2    = ps("h2",   fontSize=9,  fontName="Helvetica-Bold", textColor=SF_NAVY, spaceAfter=2, spaceBefore=6)
CODE  = ps("code", fontSize=8,  fontName="Courier",        textColor=SF_NAVY)
TH    = ps("th",   fontSize=8,  fontName="Helvetica-Bold", textColor=WHITE)
TD    = ps("td",   fontSize=7,  fontName="Helvetica",      textColor=colors.black, leading=10)
TD_B  = ps("tdb",  fontSize=7,  fontName="Helvetica-Bold", textColor=colors.black, leading=10)


def p(text, style=BODY):
    return Paragraph(text, style)


def section(text):
    return Table([[Paragraph(f"<font color='white'><b>{text}</b></font>",
                             ps("sh2", fontSize=9, fontName="Helvetica-Bold",
                                textColor=WHITE, leading=12))]],
                 colWidths=[7.0 * inch],
                 style=[("BACKGROUND", (0, 0), (-1, -1), SF_NAVY),
                        ("TOPPADDING",    (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                        ("LEFTPADDING",   (0, 0), (-1, -1), 8)])


def tbl(headers, rows, col_widths=None, row_bg=None):
    """Build a styled table with navy header row."""
    header_row = [Paragraph(h, TH) for h in headers]
    data = [header_row]
    for i, row in enumerate(rows):
        bg = row_bg[i] if row_bg and i < len(row_bg) else (SF_GREY_BG if i % 2 == 0 else WHITE)
        data.append([Paragraph(str(c), TD) for c in row])

    style = [
        ("BACKGROUND",   (0, 0), (-1,  0), SF_NAVY),
        ("TEXTCOLOR",    (0, 0), (-1,  0), WHITE),
        ("FONTNAME",     (0, 0), (-1,  0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 7),
        ("TOPPADDING",   (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
        ("LEFTPADDING",  (0, 0), (-1, -1), 5),
        ("GRID",         (0, 0), (-1, -1), 0.3, RULE_COLOR),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
    ]
    for i in range(1, len(data)):
        bg = SF_GREY_BG if i % 2 == 1 else WHITE
        style.append(("BACKGROUND", (0, i), (-1, i), bg))
    if row_bg:
        for i, bg in enumerate(row_bg):
            if bg:
                style.append(("BACKGROUND", (0, i + 1), (-1, i + 1), bg))

    return Table(data, colWidths=col_widths,
                 style=style, hAlign="LEFT", repeatRows=1)


def build(out_path):
    W = 7.0 * inch
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.6 * inch,  bottomMargin=0.6 * inch,
    )

    story = []

    # ── Hero header ──────────────────────────────────────────────────────────
    hero = Table([[
        Paragraph("<font color='white'><b>/mdm-setup + /mdm-profile + /mdm-deploy</b></font>",
                  ps("h1", fontSize=20, fontName="Helvetica-Bold", textColor=WHITE,
                     leading=24, alignment=1)),
        ], [
        Paragraph("<font color='white'>Informatica Cloud MDM Deployment Skill | "
                  "Three-Skill System</font>",
                  ps("sub", fontSize=10, textColor=WHITE, leading=13, alignment=1)),
        ], [
        Paragraph("<font color='#5BA4CF'>Business 360 / Customer 360 SaaS | "
                  "Validated: MDM-TEST-001-20261026, PROFILE-TEST-001</font>",
                  ps("val", fontSize=8, textColor=colors.HexColor("#5BA4CF"),
                     leading=11, alignment=1)),
    ]], colWidths=[W],
        style=[("BACKGROUND",    (0, 0), (-1, -1), SF_NAVY),
               ("TOPPADDING",    (0, 0), (-1, -1), 10),
               ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
               ("LEFTPADDING",   (0, 0), (-1, -1), 16),
               ("RIGHTPADDING",  (0, 0), (-1, -1), 16)])
    story += [hero, Spacer(1, 12)]

    # ── What It Is ───────────────────────────────────────────────────────────
    story += [p("<b>What It Is</b>", SEC_H),
              p("A guided deployment coach for Informatica Business 360 / Customer 360 SaaS. "
                "Three progressive phases produce shareable artifacts and gate the next phase. "
                "Nothing is created in the org until Phase 3 is reviewed and each step confirmed."),
              Spacer(1, 6)]

    story.append(tbl(
        ["Phase", "Skill", "Output", "Gate"],
        [
            ["1 - Use Case Alignment",  "/mdm-setup",
             "MDM_UseCase_{Client}.xlsx", "Stakeholder approval"],
            ["2 - Discovery Workbook",  "/mdm-profile",
             "MDM_Discovery_{Client}.xlsx (9 sheets)", "Red cells filled + profiling data"],
            ["3 - Deployment Coach",    "/mdm-deploy",
             "MDM_Deployment_Steps_{Client}.xlsx + session PDF", "Per-step signoff"],
        ],
        col_widths=[1.4*inch, 1.1*inch, 2.4*inch, 2.1*inch],
    ))
    story.append(Spacer(1, 12))

    # ── Test Mode ────────────────────────────────────────────────────────────
    story += [p("<b>Test Mode</b>", SEC_H),
              p("Add --test to any phase command to prefix all artifact names and org-written values "
                "with a test run ID (MDM-TEST-{NNN}-{YYYYMMDD}). Keeps test runs distinguishable "
                "in the org permanently. Appends a row to MDM_TEST_LOG.md after each phase."),
              Spacer(1, 4),
              p("/mdm-setup --test  |  /mdm-setup --test MDM-TEST-001-20261026", CODE),
              Spacer(1, 12)]

    # ── Phase 1 ──────────────────────────────────────────────────────────────
    story += [section("Phase 1 - Use Case Alignment"), Spacer(1, 6),
              p("<b>Two Entry Paths</b>", H2)]
    story.append(tbl(
        ["Path", "When to Use", "Output"],
        [
            ["A - Template",
             "Early engagement, no client documents yet",
             "Blank workbook with guided questions"],
            ["B - Document Ingestion",
             "Client docs available (system inventory, data dictionary, sample data, compliance policy)",
             "Skill extracts signals and pre-populates with confidence-coded recommendations citing source docs"],
        ],
        col_widths=[1.1*inch, 2.6*inch, 3.3*inch],
    ))
    story.append(Spacer(1, 8))

    story += [p("<b>5 Embedded Deployment Patterns</b>", H2)]
    story.append(tbl(
        ["Pattern", "Trust Ranking", "Match Strategy"],
        [
            ["Customer 360 / Unified View",
             "CRM first; engagement systems second",
             "Fuzzy name + address; email/phone secondary"],
            ["Marketing Deduplication",
             "CRM first; email platform; ad platform last",
             "Fuzzy name + address; email secondary"],
            ["Compliance / KYC / AML",
             "Compliance system first; no decay",
             "Exact identifier primary; fuzzy name fallback"],
            ["Post-M&A; Consolidation",
             "Acquiring org first; acquired second",
             "Fuzzy name + address (no shared identifier)"],
            ["Data Migration Hub",
             "Legacy first, flip to target over time",
             "Exact legacy key; fuzzy fallback"],
        ],
        col_widths=[1.6*inch, 2.2*inch, 3.2*inch],
    ))
    story.append(Spacer(1, 12))

    # ── Phase 2 ──────────────────────────────────────────────────────────────
    story += [section("Phase 2 - Discovery Workbook (9 Sheets)"), Spacer(1, 6)]
    story.append(tbl(
        ["Sheet", "Contents"],
        [
            ["1 Use Case",
             "Business objective, deployment pattern, assumptions, sign-off"],
            ["2 Source Systems",
             "Internal IDs (immutable warning), trust ranking, decay flag"],
            ["3 Data Model",
             "Custom field groups, field types, fgid column plan, Date vs DateTime decision"],
            ["4 Survivorship",
             "Source ranking table + decay rules (Max/Min score, Unit, Period, Pattern)"],
            ["5 DQ Planning",
             "Per-field rule plan (Basic/Advanced/DaaS), severity, trust downgrade %, "
             "DaaS entitlement check, blank-canvas prerequisites (fullName concat)"],
            ["6 Match Model",
             "Predefined vs custom decision, match criterion, population, M&M job name"],
            ["7 Data Loading",
             "CDI vs File Import decision; CDI: Secure Agent, connections, per-source mapping config; "
             "File Import: fgid plan"],
            ["8 Success Criteria",
             "9-step verification checklist; use case validation row"],
            ["9 Profiling Results",
             "IDMC Data Profiling export - grounds survivorship ranking and DQ rule selection"],
        ],
        col_widths=[1.1*inch, 5.9*inch],
    ))
    story += [Spacer(1, 4),
              p("Color coding: Red = required (must fill) | Yellow = recommended (review) | "
                "White = confirmed / pre-filled | Green = carried forward from approved Use Case",
                SMALL),
              Spacer(1, 12)]

    # ── Phase 3 Pre-Flight ────────────────────────────────────────────────────
    story += [section("Phase 3 - Pre-Flight Checklist (Irreversible Actions)"), Spacer(1, 6),
              p("All irreversible actions are listed before Step 1 and repeated in a red block "
                "before the relevant step. Nothing is executed without seeing the warning first."),
              Spacer(1, 6)]
    story.append(tbl(
        ["Label", "What Cannot Be Undone", "Recovery"],
        [
            ["A", "Source System Internal ID - locked at creation; used in every API call and ingress job forever",
             "None - prevention only"],
            ["B", "Survivorship must be configured before records exist - trust scores not retroactively recalculated",
             "Re-ingest affected records"],
            ["C", "Match model must be Published before loading - records loaded before publish have no match keys",
             "Publish + Regenerate Match Keys"],
            ["D", "Match rule cannot be edited after save - Match Strategy and Criterion are locked",
             "Delete and recreate"],
            ["E", "Predefined assets cannot be deleted (c360.person, person.ruleset1, Default, Informatica Customer 360)",
             "None"],
            ["F", "Field groups deleted after records are loaded drops all data in those fields",
             "Reload all records"],
            ["G", "Custom entity requires UI assets (Search Layout, View/Edit Page, Create Page) before Business Application association",
             "Create assets in correct order"],
            ["H", "Required field and dependency audit - Identifier field group dependencies must be resolved before File Import",
             "Delete unwanted auto-mappings in mapper"],
            ["I", "Custom entity: Subscribed Record Type and Business ID Format cannot change after records are loaded",
             "Purge all records or contact support"],
        ],
        col_widths=[0.4*inch, 4.3*inch, 2.3*inch],
    ))
    story.append(Spacer(1, 12))

    # ── Phase 3 Steps ─────────────────────────────────────────────────────────
    story += [section("Phase 3 - 9 Deployment Steps"), Spacer(1, 6)]
    story.append(tbl(
        ["#", "Type", "Step Name", "Key Notes"],
        [
            ["1",  "UI", "Create Source Systems",
             "Internal ID confirmed in dialog before Create - immutable after."],
            ["2",  "UI", "Extend Data Model",
             "Add custom field groups. Date vs DateTime choice is irreversible. "
             "Types: Text, Double, Integer, Date (yyyy-MM-dd), DateTime (yyyy-MM-dd HH:mm:ss)."],
            ["2b", "UI", "Custom Entity: Build UI Assets",
             "Blank-canvas only. Entity creation + standard fields (Person_Name, Address, Phone, "
             "Electronic Address, Full Name). Then: Search Layout, View/Edit Page, Create Page, "
             "Business Application association (Search/Pages first, Model last)."],
            ["3",  "UI", "Configure Survivorship",
             "Select entity checkbox, Edit All, Override, add sources by rank, Apply, Save. "
             "Must complete before any records exist."],
            ["4",  "UI", "Configure Data Quality",
             "Driven by DQ Planning sheet (Sheet 5). Order: fullName concat (blank-canvas prereq) "
             "then Basic rules then Advanced then DaaS. Severity + trust downgrade % per rule. "
             "DaaS Address included; Name Standardization requires separate entitlement. "
             "Rules do not apply retroactively."],
            ["5",  "UI", "Configure and Publish Match Model",
             "PATH A (custom entity): create match model from scratch using Directed AI rule wizard. "
             "Tabs: 1=Properties, 2=Required Fields, 3=Optional Fields (Attribute_1/Attribute_2), "
             "4=nothing. Publish for empty entity; Publish+Regenerate only if records already exist. "
             "PATH B (predefined entity): select person.ruleset1."],
            ["5b", "UI", "Generate Search Indexes",
             "Blank-canvas only. Skip causes index error on first File Import. "
             "B360 New, Jobs, Generate Search Indexes, Source record type, Run."],
            ["6",  "UI", "Load Data",
             "File Import (pre-deployment validation): fgid columns named {fieldGroupInternalId}_fgid. "
             "Never leave Source System as Default. "
             "CDI (production pipeline — separate downstream project): confirm Secure Agent running, "
             "create connection per source, build IDMC mapping "
             "(Source + Expression for constants + Business 360 Connector target), "
             "map field groups as {groupId}.{fieldId}, Publish each mapping before running."],
            ["7",  "UI", "Run Ingress Job",
             "Stages: Extract, Stage, Cleanse/Transform (DQ fires), Load, Index, "
             "Generate Match Keys. All sources must complete before Step 8."],
            ["8",  "UI + Script", "Define and Run Match and Merge",
             "Fields: Display Name, Process (MDMMatchMerge), Process Type, Business Entity, "
             "Match Model Name, Match Model Version, Skip grouping (leave unchecked)."],
            ["9",  "Script", "Verify Golden Records",
             "Source Records tab shows contributing sources. If tab is missing: add Source Records "
             "component to View/Edit page in Business Application Pages tab."],
        ],
        col_widths=[0.3*inch, 0.7*inch, 1.4*inch, 4.6*inch],
    ))
    story.append(Spacer(1, 12))

    # ── Step Interaction Format ───────────────────────────────────────────────
    story += [section("Step Interaction Format (Micro-Step Coaching)"), Spacer(1, 6),
              p("Each step is broken into micro-exchanges. The coach gives one action at a time "
                "and waits for a response before proceeding. Never dumps the full step at once."),
              Spacer(1, 6)]
    story.append(tbl(
        ["Phase", "What the coach does"],
        [
            ["Orient",   "One sentence: what this step does and why it matters for {Client}"],
            ["Navigate", "Exact path (every click). Describe screen from documented experience, "
                         "give the action directly, ask Done?"],
            ["Act",      "One action with exact field name and value from workbook. Done?"],
            ["React",    "If response is unexpected: diagnose before giving next action"],
            ["Verify",   "Confirm outcome before closing the step"],
            ["Signoff",  "2-4 bullet summary + carry-forward note + Name to sign off?"],
        ],
        col_widths=[0.8*inch, 6.2*inch],
    ))
    story.append(Spacer(1, 8))
    story.append(tbl(
        ["Input", "What Happens"],
        [
            ["[help]", "Question answered in 2-4 sentences with doc citation, then re-oriented in one line"],
            ["[skip]", "Steps 1-5: blocked with specific risk from Pre-Flight. Steps 6-9: allowed with note recorded."],
            ["Name",   "Updates MDM_Deployment_Session_{Client}.json + .md; regenerates full session PDF"],
        ],
        col_widths=[0.8*inch, 6.2*inch],
    ))
    story.append(Spacer(1, 12))

    # ── Artifacts Produced ────────────────────────────────────────────────────
    story += [section("Artifacts Produced"), Spacer(1, 6)]
    story.append(tbl(
        ["Artifact", "Format", "When", "Purpose"],
        [
            ["MDM_UseCase_{Client}.xlsx",           "Excel", "Phase 1",
             "Business alignment - share with stakeholders"],
            ["MDM_UseCase_{Client}_APPROVED.pdf",   "PDF",   "confirm command",
             "Locked approved record"],
            ["MDM_Discovery_{Client}.xlsx",         "Excel", "Phase 2",
             "Technical configuration workbook (9 sheets)"],
            ["MDM_Deployment_Steps_{Client}.xlsx",  "Excel", "Phase 3 start",
             "Step reference workbook (write-once, resync on resume)"],
            ["MDM_Deployment_Session_{Client}.pdf", "PDF",   "After each signoff",
             "Running deployment record - regenerated in full after every step"],
            ["MDM_Deployment_Session_{Client}.md",  "MD",    "After each signoff",
             "Human-readable audit log"],
            ["MDM_Deployment_Session_{Client}.json","JSON",  "After each signoff",
             "Machine-readable state driving PDF generation"],
        ],
        col_widths=[2.1*inch, 0.55*inch, 1.1*inch, 3.25*inch],
    ))
    story.append(Spacer(1, 12))

    # ── Supporting Scripts ────────────────────────────────────────────────────
    story += [section("Supporting Scripts"), Spacer(1, 6)]
    story.append(tbl(
        ["Script", "Status", "Purpose"],
        [
            ["mdm_scan_org.py",            "Ready",
             "Read-only org diagnostic - entity, source systems, match model, record count"],
            ["mdm_session_pdf.py",         "Ready",
             "Reads session JSON, regenerates full deployment PDF with step signoff status"],
            ["mdm_overview_pdf.py",        "Ready",
             "Regenerates this overview document"],
            ["mdm_seed_records.py",        "Pending",
             "Seed entity via Business Entity REST API (up to 50 records, CSV or manual)"],
            ["mdm_trigger_match_merge.py", "Pending",
             "POST to jobInstance/MatchMerge, poll to terminal state"],
            ["mdm_verify_records.py",      "Pending",
             "Search all records, consolidation status, source xref verification"],
            ["mdm_fetch_profile_results.py","Pending",
             "Pull IDMC Data Profiling results via REST API, write to Profiling Results sheet"],
        ],
        col_widths=[1.8*inch, 0.6*inch, 4.6*inch],
    ))
    story.append(Spacer(1, 12))

    # ── Live Validation ───────────────────────────────────────────────────────
    story += [section("Live Validation"), Spacer(1, 6)]

    story += [p("<b>MDM-TEST-001-20261026 — Full Deployment (Phases 1–3)</b>", H2),
              p("Full blank-canvas deployment completed against a production Informatica Cloud org. "
                "Customer FSI entity covering FSI banking scenario: ORION wealth management, "
                "ENCOMPASS mortgage origination, FISERVER retail banking."),
              Spacer(1, 4)]
    story.append(tbl(
        ["Check", "Result"],
        [
            ["Source systems created",     "test_orion_wealth, test_encompass_loans, test_fiserv_core_banking"],
            ["Entity type",                "Blank-canvas custom entity (not a copy of c360.person - smart fields excluded)"],
            ["Source records loaded",      "32 (ORION: 10, ENCOMPASS: 10, FISERVER: 12)"],
            ["Golden records after M+M",   "17 (15 merges)"],
            ["James Morrison verification","3 contributing source systems confirmed on one golden record"],
            ["Match model",                "customer_fsi_match v1 - Fuzzy Resident + Exact Email rules"],
            ["DQ rule",                    "Concat Full Name (firstName + lastName to fullName) feeding match keys"],
        ],
        col_widths=[2.0*inch, 5.0*inch],
    ))
    story.append(Spacer(1, 10))

    story += [p("<b>PROFILE-TEST-001 — /mdm-profile Validation</b>", H2),
              p("End-to-end /mdm-profile skill run producing profiling workbook and DQ rule plan "
                "for a three-source FSI scenario: ORION wealth management, ENCOMPASS loan origination, "
                "FiServ core banking."),
              Spacer(1, 4)]
    story.append(tbl(
        ["Check", "Result"],
        [
            ["Workbook produced",          "MDM_Profile_DQ_FSI.xlsx — 7 sheets"],
            ["Sources profiled",           "ORION, ENCOMPASS, FiServ (3 sources)"],
            ["Primary source (Rank 1)",    "FiServ — 98.7% completeness"],
            ["DQ rules planned",           "8 rules across Basic, DaaS categories; trust downgrade % set per findings"],
            ["CDI Transformations sheet",  "Per-source field mapping plan carried forward to Sheet 7 of Discovery workbook"],
        ],
        col_widths=[2.0*inch, 5.0*inch],
    ))
    story.append(Spacer(1, 12))

    # ── Footer ────────────────────────────────────────────────────────────────
    footer = Table([[
        Paragraph(
            "All guidance grounded in official Informatica documentation. "
            "Every irreversible action cites source doc and page. "
            "Nothing is created in the org until Phase 3 is reviewed and each step is confirmed.",
            ps("ft", fontSize=7, textColor=colors.HexColor("#888888"), alignment=1, leading=10))
    ]], colWidths=[W],
        style=[("TOPPADDING",    (0, 0), (-1, -1), 4),
               ("BOTTOMPADDING", (0, 0), (-1, -1), 4)])
    story.append(footer)

    doc.build(story)
    print(f"✓ Overview PDF generated: {out_path}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
        "~/Downloads/MDM_Setup_Skill_Overview.pdf")
    build(out)
