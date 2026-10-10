"""
mdm_scan_org.py — Read-only MDM org state scanner.

Checks:
  - c360.person entity accessible
  - person.ruleset1 match model publication status
  - Existing source systems (names + internal IDs)
  - Record count in c360.person
  - Existing Match & Merge job definitions

Makes NO changes to the org. Safe to run at any time.
"""

import json
import sys
import getpass
import time
import urllib.request
import urllib.error


def login(base_url, username, password):
    url = f"{base_url}/saas/public/core/v3/login"
    payload = json.dumps({"username": username, "password": password}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    session_id = data["userInfo"]["sessionId"]
    api_url = data["products"][0]["baseApiUrl"].replace("/saas", "").replace("use4", "use4-mdm")
    return session_id, api_url


def get(api_url, path, session_id):
    url = f"{api_url}{path}"
    req = urllib.request.Request(url, headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "IDS-SESSION-ID": session_id,
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read()), resp.status
    except urllib.error.HTTPError as e:
        return None, e.code


def post(api_url, path, session_id, payload):
    url = f"{api_url}{path}"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "IDS-SESSION-ID": session_id,
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read()), resp.status
    except urllib.error.HTTPError as e:
        return None, e.code


def main():
    print("=" * 60)
    print("  MDM Org Scanner — Read-Only Diagnostic")
    print("=" * 60)
    print()

    base_url = input("IDMC org URL (e.g. https://dm-us.informaticacloud.com): ").strip().rstrip("/")
    username = input("IDMC username (email): ").strip()
    password = getpass.getpass("Password: ")

    print()
    print("Authenticating...")
    try:
        session_id, api_url = login(base_url, username, password)
        print(f"  ✓ Authenticated — MDM API base: {api_url}")
    except Exception as e:
        print(f"  ✗ Authentication failed: {e}")
        sys.exit(1)

    print()
    print("-" * 60)
    print("SECTION 1 — Business Entity: c360.person")
    print("-" * 60)

    entity_resp, status = get(api_url, "/business-entity/public/api/v1/metadata/entity/c360.person", session_id)
    if status == 200 and entity_resp:
        print("  ✓ c360.person exists and is accessible")
    elif status == 404:
        print("  ✗ c360.person NOT FOUND — Customer 360 SaaS may not be provisioned in this org")
    else:
        print(f"  ? c360.person check returned HTTP {status}")

    print()
    print("-" * 60)
    print("SECTION 2 — Match Model: person.ruleset1")
    print("-" * 60)

    mm_resp, status = get(api_url, "/business-entity/public/api/v1/metadata/matchModel?businessEntity=c360.person", session_id)
    if status == 200 and mm_resp:
        models = mm_resp if isinstance(mm_resp, list) else mm_resp.get("matchModels", [])
        if not models:
            print("  ✗ No match models found for c360.person")
        for m in models:
            name = m.get("name") or m.get("id", "unknown")
            state = m.get("status") or m.get("state", "unknown")
            version = m.get("version", "")
            marker = "✓" if state.upper() == "PUBLISHED" else "⚠"
            print(f"  {marker} {name}  |  status: {state}  |  version: {version}")
    else:
        print(f"  ? Match model query returned HTTP {status} — check manually in Business 360 Console")
        print("    UI path: c360.person → Match tab → look for person.ruleset1")

    print()
    print("-" * 60)
    print("SECTION 3 — Source Systems")
    print("-" * 60)

    ss_resp, status = get(api_url, "/business-entity/public/api/v1/metadata/sourceSystem", session_id)
    if status == 200 and ss_resp:
        systems = ss_resp if isinstance(ss_resp, list) else ss_resp.get("sourceSystems", [])
        if not systems:
            print("  (No source systems found — only predefined defaults)")
        for s in systems:
            name = s.get("displayName") or s.get("name", "unknown")
            internal_id = s.get("name") or s.get("id", "unknown")
            predefined = s.get("predefined", False)
            tag = " [predefined — cannot delete]" if predefined else ""
            print(f"  • {name}  (internal ID: {internal_id}){tag}")
    else:
        print(f"  ? Source system query returned HTTP {status}")

    print()
    print("-" * 60)
    print("SECTION 4 — Record Count in c360.person")
    print("-" * 60)

    search_payload = {"search": "*", "entityType": "c360.person", "pageSize": 1}
    search_resp, status = post(api_url, "/search/public/api/v1/search", session_id, search_payload)
    if status == 200 and search_resp:
        total = search_resp.get("totalCount") or search_resp.get("count", "unknown")
        if total == 0:
            print(f"  ✓ Records in c360.person: 0 (clean start)")
        else:
            print(f"  ⚠ Records in c360.person: {total}")
            print("    NOTE: If survivorship has not been configured, these records")
            print("    used default (no) survivorship. Verify with org admin.")
    else:
        print(f"  ? Record count query returned HTTP {status}")

    print()
    print("-" * 60)
    print("SECTION 5 — Existing Match & Merge Job Definitions")
    print("-" * 60)

    jobs_resp, status = get(api_url, "/job/public/api/v1/jobDefinition?type=MatchMerge", session_id)
    if status == 200 and jobs_resp:
        jobs = jobs_resp if isinstance(jobs_resp, list) else jobs_resp.get("jobDefinitions", [])
        if not jobs:
            print("  (No Match & Merge job definitions found — will need to create in Step 5)")
        for j in jobs:
            name = j.get("displayName") or j.get("name", "unknown")
            jid = j.get("id") or j.get("jobDefinitionId", "unknown")
            print(f"  • {name}  (jobDefinitionId: {jid})")
    else:
        print(f"  ? Job definition query returned HTTP {status}")

    print()
    print("=" * 60)
    print("  Scan complete — no changes were made to the org")
    print("=" * 60)


if __name__ == "__main__":
    main()
