from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDS_FILE = "tools/credentials.json"
SHEET_ID   = "11SzrA-74qZgYW9JXpe7LMXb8bDqxSQmL05X6VLYeLcA"
SHEET_NAME = "cards_master"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds   = service_account.Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)
sheet   = service.spreadsheets()

# ── 1. Read all existing data ─────────────────────────────────────────────────
result = sheet.values().get(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME}!A:G"
).execute()
rows = result.get("values", [])

print(f"Read {len(rows)} rows (including header)")

# ── 2. Build new data ─────────────────────────────────────────────────────────
# New columns order:
# id | deck | unit | question | answer | distractor_1 | distractor_2 | distractor_3
# | card_type | needs_image | tags | suspended | notes

new_header = [
    "id", "deck", "unit", "question", "answer",
    "distractor_1", "distractor_2", "distractor_3",
    "card_type", "needs_image", "tags", "suspended", "notes"
]

new_rows = [new_header]

for i, row in enumerate(rows[1:], start=2):  # skip old header, track row number
    # Pad row to 7 columns in case trailing cells are missing
    while len(row) < 7:
        row.append("")

    card_id      = row[0]
    deck         = row[1]
    question     = row[2]
    answer       = row[3]
    distractor_1 = row[4]
    distractor_2 = row[5]
    distractor_3 = row[6]

    # Derive a sensible tag from the deck name
    # e.g. "trig values sin cos radians" -> "trig"
    # "squares and square roots"         -> "squares"
    # "higher powers"                    -> "higher-powers"
    tag = deck.split()[0] if deck else ""

    new_row = [
        card_id,
        deck,
        "",           # unit — blank for non-AP-Calc cards
        question,
        answer,
        distractor_1,
        distractor_2,
        distractor_3,
        "basic",      # card_type — all existing cards are basic
        "FALSE",      # needs_image
        tag,          # tags — simple deck-derived tag for now
        "FALSE",      # suspended
        "",           # notes
    ]
    new_rows.append(new_row)

print(f"Built {len(new_rows)} rows (including header)")

# ── 3. Clear and rewrite the sheet ───────────────────────────────────────────
sheet.values().clear(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME}!A:Z"
).execute()

sheet.values().update(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME}!A1",
    valueInputOption="RAW",
    body={"values": new_rows}
).execute()

print("✅ Sheet redesigned successfully!")
print(f"   Columns: {', '.join(new_header)}")
print(f"   Total data rows: {len(new_rows) - 1}")