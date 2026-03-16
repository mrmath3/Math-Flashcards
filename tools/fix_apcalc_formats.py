import os
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDS_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")
SPREADSHEET_ID = "11SzrA-74qZgYW9JXpe7LMXb8bDqxSQmL05X6VLYeLcA"
SHEET = "cards_master"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def is_latex(value):
    """Returns True if value contains LaTeX indicators."""
    if not isinstance(value, str):
        return False
    return bool(re.search(r'[\\^{}_]', value))

def detect_format(value):
    return "math" if is_latex(value) else "text"

def col_letter(n):
    """Convert 0-based column index to letter (0=A, 13=N, etc.)"""
    result = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        result = chr(65 + r) + result
    return result

def main():
    creds = service_account.Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # Read all data
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET}!A:P"
    ).execute()
    rows = result.get("values", [])

    header = rows[0]
    # Column indices (0-based)
    col = {h: i for i, h in enumerate(header)}
    # Expected: deck=B(1), question=D(3), answer=E(4), q_format=N(13), a_format=O(14), d_format=P(15)

    changes = []  # (sheet_row_1based, col_letter, new_value, old_value, field_name)

    for i, row in enumerate(rows[1:], start=2):  # sheet row index (1-based)
        # Pad row to full width
        while len(row) <= 15:
            row.append("")

        deck = row[col["deck"]] if "deck" in col else ""
        if deck != "AP Calculus AB":
            continue

        question = row[col["question"]] if "question" in col else ""
        answer = row[col["answer"]] if "answer" in col else ""
        q_format_current = row[col["q_format"]] if "q_format" in col else "math"
        a_format_current = row[col["a_format"]] if "a_format" in col else "math"

        q_format_new = detect_format(question)
        a_format_new = detect_format(answer)

        card_id = row[col["id"]] if "id" in col else f"row {i}"

        if q_format_new != q_format_current:
            changes.append((i, col["q_format"], q_format_new, q_format_current, "q_format", card_id, question[:40]))
        if a_format_new != a_format_current:
            changes.append((i, col["a_format"], a_format_new, a_format_current, "a_format", card_id, answer[:40]))

    if not changes:
        print("No changes needed — all AP Calc formats already correct.")
        return

    print(f"Found {len(changes)} cells to update:\n")
    for sheet_row, col_idx, new_val, old_val, field, card_id, preview in changes:
        print(f"  Row {sheet_row:3d} | {card_id:<10} | {field:<10} | {old_val} → {new_val} | \"{preview}\"")

    print(f"\nApplying {len(changes)} updates...")

    # Build batch update data
    data = []
    for sheet_row, col_idx, new_val, old_val, field, card_id, preview in changes:
        cell = f"{SHEET}!{col_letter(col_idx)}{sheet_row}"
        data.append({
            "range": cell,
            "values": [[new_val]]
        })

    body = {
        "valueInputOption": "RAW",
        "data": data
    }
    sheet.values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=body
    ).execute()

    print("Done. Run rebuild_anki_tab.py to refresh anki formulas.")

if __name__ == "__main__":
    main()
