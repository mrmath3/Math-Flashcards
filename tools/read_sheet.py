from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

CREDS_FILE = "tools/credentials.json"
SHEET_ID   = "11SzrA-74qZgYW9JXpe7LMXb8bDqxSQmL05X6VLYeLcA"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds   = service_account.Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)
sheet   = service.spreadsheets()

# ── Get sheet names ───────────────────────────────────────────────────────────
metadata = sheet.get(spreadsheetId=SHEET_ID).execute()
tab_names = [s["properties"]["title"] for s in metadata["sheets"]]
print(f"Tabs: {tab_names}\n")

# ── Read each tab ─────────────────────────────────────────────────────────────
for tab in tab_names:
    print(f"{'='*60}")
    print(f"TAB: {tab}")
    print(f"{'='*60}")

    # FORMULA view — shows raw formulas in cells
    formula_result = sheet.values().get(
        spreadsheetId=SHEET_ID,
        range=f"{tab}",
        valueRenderOption="FORMULA",
        dateTimeRenderOption="FORMATTED_STRING"
    ).execute()

    rows = formula_result.get("values", [])

    if not rows:
        print("  (empty tab)\n")
        continue

    print(f"Rows: {len(rows)}  |  Cols: {max(len(r) for r in rows)}\n")

    for i, row in enumerate(rows, start=1):
        # Only print rows that have at least one non-empty cell
        if any(cell.strip() if isinstance(cell, str) else cell for cell in row):
            print(f"  Row {i:>4}: {row}")

    print()