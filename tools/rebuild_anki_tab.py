"""
rebuild_anki_tab.py

Rebuilds the entire anki tab from scratch based on whatever rows
currently exist in cards_master. Safe to run any time — it clears
and rewrites the tab completely.

Column layout after rebuild:
  A = id
  B = deck
  C = front  (cloze string for cloze cards; format-aware question for basic cards)
  D = back   (blank for cloze cards; format-aware answer for basic cards)

Format-aware means:
  q_format = "math"  →  wraps in \\( ... \\)
  q_format = "text"  →  plain text, no wrapping

cards_master column positions (1-based):
  A=1  id
  B=2  deck
  C=3  unit
  D=4  question
  E=5  answer
  I=9  card_type
  N=14 q_format
  O=15 a_format

Usage (from any directory):
  python3 /Users/mrmath3/Documents/GitHub/Math-Flashcards/tools/rebuild_anki_tab.py
"""

import os
import gspread
from google.oauth2.service_account import Credentials
import time

# ── Auth ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(SCRIPT_DIR, "credentials.json")
SHEET_URL  = "https://docs.google.com/spreadsheets/d/11SzrA-74qZgYW9JXpe7LMXb8bDqxSQmL05X6VLYeLcA/edit"
SCOPES     = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sh     = client.open_by_url(SHEET_URL)

# ── Read cards_master to find how many data rows exist ────────────────────────
print("Reading cards_master…")
ws_cards = sh.worksheet("cards_master")
all_values = ws_cards.get_all_values()
header = all_values[0]
num_data_rows = len(all_values) - 1  # excludes header row
total_rows = len(all_values)         # includes header

print(f"  Found {num_data_rows} data rows (rows 2–{total_rows})")

# Confirm expected columns exist
col_idx = {name: i for i, name in enumerate(header)}
required = ["id", "deck", "question", "answer", "card_type", "q_format", "a_format"]
missing = [c for c in required if c not in col_idx]
if missing:
    raise ValueError(f"cards_master is missing expected columns: {missing}")

# Column letters for cards_master (1-based → letter)
def col_letter(n):
    result = ""
    while n:
        n, rem = divmod(n - 1, 26)
        result = chr(65 + rem) + result
    return result

COL = {name: col_letter(i + 1) for name, i in col_idx.items()}

print(f"  cards_master column map:")
for name in required:
    print(f"    {name:12s} → col {COL[name]}")

# ── Build formula rows ────────────────────────────────────────────────────────
# Row 1: headers (static)
header_row = [["id", "deck", "front", "back"]]

# Rows 2+: one formula row per data row in cards_master
def make_anki_row(n):
    """
    n = sheet row number in cards_master (2-based, matching actual row numbers).
    Returns a list of 4 formula strings: [id, deck, front, back]
    """
    q_col    = COL["question"]    # D
    a_col    = COL["answer"]      # E
    type_col = COL["card_type"]   # I
    qf_col   = COL["q_format"]    # N
    af_col   = COL["a_format"]    # O

    # id and deck are always simple references
    id_formula   = f"=cards_master!A{n}"
    deck_formula = f"=cards_master!B{n}"

    # ── front (col C) ──────────────────────────────────────────────────────
    # For cloze:  \(question\) = {{c1::\(answer\)}}   (or text variants)
    # For basic:  \(question\)                         (or plain text)
    #
    # q_part: IF q_format="math" → "\("&question&"\)"  ELSE question
    q_part = (
        f'IF(cards_master!{qf_col}{n}="math",'
        f'"\\("&cards_master!{q_col}{n}&"\\)",'
        f'cards_master!{q_col}{n})'
    )

    # a_part (used only in cloze front): IF a_format="math" → {{c1::\(answer\)}} ELSE {{c1::answer}}
    a_part_cloze = (
        f'IF(cards_master!{af_col}{n}="math",'
        f'"{{{{c1::\\("&cards_master!{a_col}{n}&"\\)}}}}",'
        f'"{{{{c1::"&cards_master!{a_col}{n}&"}}}}")'
    )

    # front formula:
    #   IF card_type="cloze" → q_part & " = " & a_part_cloze
    #   ELSE (basic)         → q_part
    front_formula = (
        f'=IF(cards_master!{type_col}{n}="cloze",'
        f'{q_part}&" = "&{a_part_cloze},'
        f'{q_part})'
    )

    # ── back (col D) ───────────────────────────────────────────────────────
    # For cloze: blank (Anki ignores the back field for cloze notes)
    # For basic: IF a_format="math" → \(answer\)  ELSE answer
    a_part_basic = (
        f'IF(cards_master!{af_col}{n}="math",'
        f'"\\("&cards_master!{a_col}{n}&"\\)",'
        f'cards_master!{a_col}{n})'
    )

    back_formula = (
        f'=IF(cards_master!{type_col}{n}="cloze",'
        f'"",'
        f'{a_part_basic})'
    )

    return [id_formula, deck_formula, front_formula, back_formula]

data_rows = [make_anki_row(n) for n in range(2, total_rows + 1)]
all_rows = header_row + data_rows

print(f"\nBuilt {len(data_rows)} formula rows.")

# ── Clear and rewrite the anki tab ────────────────────────────────────────────
print("Clearing anki tab…")
ws_anki = sh.worksheet("anki")
ws_anki.clear()
time.sleep(1)

# Write in chunks to avoid API payload limits (each row has 4 cells)
CHUNK_SIZE = 200   # rows per batch
print(f"Writing {len(all_rows)} rows in chunks of {CHUNK_SIZE}…")

for i in range(0, len(all_rows), CHUNK_SIZE):
    chunk = all_rows[i:i + CHUNK_SIZE]
    start_row = i + 1  # 1-based
    end_row   = start_row + len(chunk) - 1
    range_str = f"A{start_row}:D{end_row}"
    ws_anki.update(chunk, range_str, value_input_option="USER_ENTERED")
    time.sleep(0.5)
    print(f"  Wrote rows {start_row}–{end_row}")

print(f"\n✅ anki tab rebuilt successfully.")
print(f"   Rows: 1 header + {len(data_rows)} card rows = {len(all_rows)} total")
print(f"   Columns: A=id  B=deck  C=front  D=back")
print(f"\nRun 'readsheet' from the repo root to verify.")
