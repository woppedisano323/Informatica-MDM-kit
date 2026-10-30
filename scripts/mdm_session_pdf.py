"""
mdm_session_pdf.py — Regenerate the MDM deployment session PDF from a session JSON file.

Called after every step signoff. Always regenerates the full PDF so it reflects
current state and can be shared at any point mid-deployment.

Usage:
    python3 mdm_session_pdf.py <path/to/MDM_Deployment_Session_<Client>.json>

Session JSON schema:
{
  "client":  "Apex Financial Services",
  "org":     "https://dm-us.informaticacloud.com",
  "pattern": "Customer 360 / Unified Customer View",
  "entity":  "c360.person",
  "started": "2026-10-10",
  "output_dir": "~/Downloads/",
  "steps": [
    {
      "number": 1,
      "name": "Create Source Systems",
      "status": "complete",          // complete | in_progress | skipped | pending
      "completed_date": "2026-10-10",
      "signed_off_by": "Will Oppedisano",
      "table": {
        "headers": ["Source System", "Internal ID", "Trust Level"],
        "rows": [["Salesforce CRM", "salesforce_crm", "Rank 1"]]
      },
      "notes": ["Optional note shown below the table"]
    },
    ...
  ]
}
"""

import json
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
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
SF_GREEN_HDR= colors.HexColor("#C8E6C9")
SF_AMBER    = colors.HexColor("#F57C00")
SF_AMBER_BG = colors.HexColor("#FFF3E0")
SF_GREY     = colors.HexColor("#B0BEC5")
SF_GREY_BG  = colors.HexColor("#F5F5F5")
WHITE       = colors.white
RULE_COLOR  = colors.HexColor("#E0E0E0")
NOTE_COLOR  = colors.HexColor("#555555")


def ps(name, **kwargs):
    defaults = dict(fontSize=8, fontName="Helvetica", textColor=colors.black, leading=11)
    defaults.update(kwargs)
    return ParagraphStyle(name, **defaults)


LABEL  = ps("lbl", fontName="Helvetica-Bold", textColor=SF_NAVY)
VAL    = ps("val")
NOTE   = ps("note", fontName="Helvetica-Oblique", textColor=NOTE_COLOR)
PEND   = ps("pend", textColor=SF_GREY)
SEC_HD = ps("sh", fontSize=10, fontName="Helvetica-Bold", textColor=SF_NAVY, spaceAfter=4)


def section_header(text):
    return Paragraph(f"<font color='#032D60'><b>{text}</b></font>", SEC_HD)


def signed_badge(name, date):
    return Paragraph(
        f"<font color='#2E7D32'><b>✓ Signed off by {name}</b></font>"
        f"  <font color='#555555'>{date}</font>",
        ps("badge", textColor=SF_GREEN),
    )


def step_table(table_data):
    if not table_data:
        return None
    headers = table_data.get("headers", [])
    rows = table_data.get("rows", [])
    col_count = len(headers)
    if col_count == 0:
        return None

    page_width = 7 * inch
    col_width = page_width / col_count

    data = [[Paragraph(h, LABEL) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(cell), VAL) for cell in row])

    tbl = Table(data, colWidths=[col_width] * col_count)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SF_GREEN_BG),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.5, SF_GREEN_HDR),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tbl


def in_progress_bar(notes):
    note_text = notes[0] if notes else "In progress"
    bar = Table([[
        Paragraph(
            f"<font color='#F57C00'><b>⬤ In Progress</b></font>"
            f"  <font color='#555555'>{note_text}</font>",
            ps("ip", textColor=SF_AMBER),
        )
    ]], colWidths=[7 * inch])
    bar.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SF_AMBER_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return bar


def skipped_bar(notes):
    note_text = notes[0] if notes else "Skipped"
    bar = Table([[
        Paragraph(
            f"<font color='#555555'><b>⏭ Skipped</b></font>"
            f"  <font color='#888888'>{note_text}</font>",
            ps("sk", textColor=NOTE_COLOR),
        )
    ]], colWidths=[7 * inch])
    bar.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SF_GREY_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return bar


def pending_bar(name):
    bar = Table([[
        Paragraph(f"<font color='#B0BEC5'>⬜  {name}</font>", PEND)
    ]], colWidths=[7 * inch])
    bar.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SF_GREY_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return bar


def build_pdf(session, out_path):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
    )

    steps = session.get("steps", [])
    completed = sum(1 for s in steps if s.get("status") == "complete")
    total = len(steps)

    story = []

    # Header banner
    hdr = Table([[
        Paragraph(
            "<font color='white'><b>MDM Deployment Session</b><br/>"
            f"{session['client']}</font>",
            ps("hdr", fontSize=16, leading=20, textColor=WHITE),
        ),
        Paragraph(
            f"<font color='white'>Org: {session.get('org','')}<br/>"
            f"Pattern: {session.get('pattern','')}<br/>"
            f"Entity: {session.get('entity','')}"
            f"   |   Started: {session.get('started','')}</font>",
            ps("hdr2", fontSize=9, leading=13, textColor=WHITE),
        ),
    ]], colWidths=[3.2 * inch, 3.8 * inch])
    hdr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SF_NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 14))

    # Progress bar
    pending_count = total - completed
    src_file = f"MDM_Discovery_{session['client'].replace(' ','_')}.xlsx"
    prog = Table([[
        Paragraph(f"<b>{completed} of {total} steps signed off</b>", ps("pb", fontName="Helvetica-Bold", textColor=SF_NAVY)),
        Paragraph(f"{pending_count} steps pending", ps("pb2", textColor=SF_NAVY)),
        Paragraph(f"Source: {src_file}", ps("pb3", textColor=SF_NAVY)),
    ]], colWidths=[2 * inch, 2 * inch, 3 * inch])
    prog.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SF_LBLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(prog)
    story.append(Spacer(1, 16))

    # Step blocks
    for step in steps:
        status = step.get("status", "pending")
        step_label = f"Step {step['number']} — {step['name']}"

        if status == "complete":
            story.append(section_header(step_label))
            tbl = step_table(step.get("table"))
            if tbl:
                story.append(tbl)
                story.append(Spacer(1, 5))
            for note in step.get("notes", []):
                story.append(Paragraph(note, NOTE))
                story.append(Spacer(1, 3))
            story.append(signed_badge(step["signed_off_by"], step["completed_date"]))

        elif status == "in_progress":
            story.append(section_header(step_label))
            story.append(in_progress_bar(step.get("notes", [])))

        elif status == "skipped":
            story.append(section_header(step_label))
            story.append(skipped_bar(step.get("notes", [])))

        else:  # pending
            story.append(pending_bar(step_label))

        story.append(Spacer(1, 12))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR))
        story.append(Spacer(1, 10))

    # Footer
    footer = Table([[
        Paragraph(
            f"This document reflects deployment progress as of {session.get('started','')}. "
            "Generated by /mdm-deploy. To revise, return to your MDM Deploy session.",
            ps("ft", fontSize=7, textColor=colors.HexColor("#888888")),
        )
    ]], colWidths=[7 * inch])
    footer.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SF_GREY_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(footer)

    doc.build(story)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 mdm_session_pdf.py <session.json>")
        sys.exit(1)

    json_path = os.path.expanduser(sys.argv[1])
    with open(json_path) as f:
        session = json.load(f)

    out_dir = os.path.expanduser(session.get("output_dir", "~/Downloads/"))
    client_slug = session["client"].replace(" ", "_")
    out_path = os.path.join(out_dir, f"MDM_Deployment_Session_{client_slug}.pdf")

    build_pdf(session, out_path)
    print(f"✓ PDF regenerated: {out_path}")


if __name__ == "__main__":
    main()
