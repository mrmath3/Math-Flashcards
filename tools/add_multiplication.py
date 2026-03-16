"""
add_multiplication.py

Adds 144 multiplication flashcards (1×1 through 12×12) to the cards_master
tab of the Math Flashcards Google Sheet.

Also adds three new columns to cards_master if they don't exist:
  - q_format  (math | text)
  - a_format  (math | text)
  - d_format  (math | text)

And updates the anki tab formula to respect those format flags.

Usage:
  cd /Users/mrmath3/Documents/GitHub/Math-Flashcards/tools
  python3 add_multiplication.py
"""

import gspread
from google.oauth2.service_account import Credentials
import time

# ── Auth ──────────────────────────────────────────────────────────────────────
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
CREDS_FILE  = "credentials.json"          # relative to tools/
SHEET_URL   = "https://docs.google.com/spreadsheets/d/11SzrA-74qZgYW9JXpe7LMXb8bDqxSQmL05X6VLYeLcA/edit"

creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sh     = client.open_by_url(SHEET_URL)

# ── Helpers ───────────────────────────────────────────────────────────────────
def col_letter(n):
    """Convert 1-based column index to letter(s): 1→A, 26→Z, 27→AA …"""
    result = ""
    while n:
        n, rem = divmod(n - 1, 26)
        result = chr(65 + rem) + result
    return result

def batch_update(ws, updates):
    """Send a list of Cell objects in one API call."""
    ws.update_cells(updates, value_input_option="USER_ENTERED")

# ── Mnemonics (notes column) ───────────────────────────────────────────────────
# Cute memory tricks sourced from elementary math education resources.
# Hardest facts get specific mnemonics; easy ones get pattern reminders.
MNEMONICS = {
    # Landmark/pattern facts
    (1, 1): "Any number × 1 = itself. The identity property — 1 is the 'do-nothing' multiplier!",
    (2, 2): "Double 2 is 4. Even × even is always even.",
    (5, 5): "5 × 5 = 25. Five fingers on each hand — two hands make 25 fingers? Count your fingers!",
    (10,10): "10 × 10 = 100. Just add two zeros!",
    (11,11): "11 × 11 = 121. Palindrome — reads the same forwards and backwards!",
    (12,12): "12 × 12 = 144. Called 'a gross' — a dozen dozens. Think: a gross of eggs.",
    # Twos (doubling)
    (2, 3): "2 × 3 = 6. Doubling: just add 3 + 3.",
    (2, 4): "2 × 4 = 8. Double 4 = 8. Even your spider has 8 legs — 2 groups of 4!",
    (2, 5): "2 × 5 = 10. Two hands, five fingers each — that's 10!",
    (2, 6): "2 × 6 = 12. A dozen eggs comes in 2 rows of 6.",
    (2, 7): "2 × 7 = 14. Two weeks = 14 days.",
    (2, 8): "2 × 8 = 16. A spider has 8 legs — two spiders have 16.",
    (2, 9): "2 × 9 = 18. Double 9 — think of 18 holes on a golf course.",
    (2,10): "2 × 10 = 20. Two dimes = 20 cents.",
    (2,11): "2 × 11 = 22. The number repeats itself!",
    (2,12): "2 × 12 = 24. Two dozen donuts = 24.",
    # Fives (clock trick)
    (5, 1): "5 × 1 = 5. Fives always end in 0 or 5.",
    (5, 2): "5 × 2 = 10. Count by 5s on a clock: 5, 10!",
    (5, 3): "5 × 3 = 15. Three nickels = 15 cents.",
    (5, 4): "5 × 4 = 20. Four nickels = 20 cents.",
    (5, 6): "5 × 6 = 30. Six nickels = 30 cents. Halfway around the clock!",
    (5, 7): "5 × 7 = 35. Seven nickels = 35 cents.",
    (5, 8): "5 × 8 = 40. Eight nickels = 40 cents.",
    (5, 9): "5 × 9 = 45. Nine nickels = 45 cents.",
    (5,10): "5 × 10 = 50. Ten nickels = 50 cents — half a dollar!",
    (5,11): "5 × 11 = 55. Eleven nickels = 55 cents.",
    (5,12): "5 × 12 = 60. Sixty seconds in a minute — 12 groups of 5!",
    # Nines (finger trick)
    (9, 1): "9 × 1 = 9. Nines trick: digits always add up to 9.",
    (9, 2): "9 × 2 = 18. 1 + 8 = 9. ✓ Digit sum check!",
    (9, 3): "9 × 3 = 27. 2 + 7 = 9. ✓",
    (9, 4): "9 × 4 = 36. 3 + 6 = 9. ✓ Try the finger trick: fold down finger 4.",
    (9, 5): "9 × 5 = 45. 4 + 5 = 9. ✓",
    (9, 6): "9 × 6 = 54. 5 + 4 = 9. ✓",
    (9, 7): "9 × 7 = 63. 6 + 3 = 9. ✓",
    (9, 8): "9 × 8 = 72. 7 + 2 = 9. ✓",
    (9, 9): "9 × 9 = 81. 8 + 1 = 9. ✓ 9 is the biggest single-digit number and likes to show off!",
    (9,10): "9 × 10 = 90. 9 + 0 = 9. ✓",
    (9,11): "9 × 11 = 99. Almost 100 — just 1 short!",
    (9,12): "9 × 12 = 108. 1 + 0 + 8 = 9. ✓ Digit sum still works!",
    # Elevens trick
    (11, 1): "11 × 1 = 11. Eleven just copies the digit: 11×1=11, 11×2=22…",
    (11, 2): "11 × 2 = 22. The digit doubles itself.",
    (11, 3): "11 × 3 = 33.",
    (11, 4): "11 × 4 = 44.",
    (11, 5): "11 × 5 = 55.",
    (11, 6): "11 × 6 = 66.",
    (11, 7): "11 × 7 = 77.",
    (11, 8): "11 × 8 = 88.",
    (11, 9): "11 × 9 = 99.",
    (11,10): "11 × 10 = 110.",
    (11,12): "11 × 12 = 132. For 11 × two-digit numbers: add the digits and put the sum in the middle. 1+2=3, so 132.",
    # Twelves
    (12, 1): "12 × 1 = 12. One dozen.",
    (12, 2): "12 × 2 = 24. Two dozen = 24 (donuts!).",
    (12, 3): "12 × 3 = 36. Three dozen = 36.",
    (12, 4): "12 × 4 = 48. Four dozen = 48.",
    (12, 5): "12 × 5 = 60. Five dozen = 60 seconds in a minute!",
    (12, 6): "12 × 6 = 72. Six dozen = 72.",
    (12, 7): "12 × 7 = 84. Seven dozen = 84.",
    (12, 8): "12 × 8 = 96. Eight dozen = 96.",
    (12, 9): "12 × 9 = 108. Nine dozen = 108.",
    (12,10): "12 × 10 = 120. Ten dozen = 120.",
    # Hardest facts (3–9 range) — specific mnemonics
    (3, 6): "3 × 6 = 18. Three and six went on a date, ended up with eighteen!",
    (3, 7): "3 × 7 = 21. 3, 7 — 'three and seven make twenty-one' (like the card game blackjack!).",
    (3, 8): "3 × 8 = 24. 3 × 8 = 24. Think: 3 bundles of 8 crayons = 24 crayons.",
    (3, 9): "3 × 9 = 27. 3, 9 — 27. Digit sum: 2 + 7 = 9. ✓",
    (4, 6): "4 × 6 = 24. Four and six went to pick up sticks — they picked up 24!",
    (4, 7): "4 × 7 = 28. 4 weeks = 28 days in February!",
    (4, 8): "4 × 8 = 32. 4 × 8 = 32. Think: 4 spiders × 8 legs = 32 legs.",
    (4, 9): "4 × 9 = 36. 9 × 4 = 36. Digit sum: 3 + 6 = 9. ✓",
    (6, 6): "6 × 6 = 36. Six sticks, six sticks = 36 sticks. Or: a 6×6 ice cube tray has 36 cubes.",
    (6, 7): "6 × 7 = 42. 'Six and seven went to heaven, came back with forty-two.'",
    (6, 8): "6 × 8 = 48. 'Six ate (8) forty-eight cookies and got sick!' 6 × 8 = 48.",
    (6, 9): "6 × 9 = 54. Digit sum: 5 + 4 = 9. ✓ Also: switch the digits of 9×6: 9,6 → 54.",
    (7, 7): "7 × 7 = 49. 'Seven squared is forty-nine — lucky sevens land on 49!'",
    (7, 8): "7 × 8 = 56. The magic sequence: 5, 6, 7, 8 — the answer (56) uses the two numbers right before 7 and 8!",
    (7, 9): "7 × 9 = 63. Digit sum: 6 + 3 = 9. ✓ Think: 63 has the digits 6 and 3, and 7−1=6, 10−7=3.",
    (8, 8): "8 × 8 = 64. 'I ate and ate and got sick on the floor — 8 × 8 = 64!'",
    (8, 9): "8 × 9 = 72. Digit sum: 7 + 2 = 9. ✓ Think: 8 × 9 = (8×10) − 8 = 80 − 8 = 72.",
}

def get_note(a, b):
    """Return mnemonic for a×b, checking both orderings."""
    return (MNEMONICS.get((a, b))
            or MNEMONICS.get((b, a))
            or f"{a} × {b} = {a*b}. Practice skip-counting by {min(a,b)}s to verify!")

# ── Distractor logic ──────────────────────────────────────────────────────────
# Build full set of valid products for the 1–12 table.
ALL_PRODUCTS = set()
for i in range(1, 13):
    for j in range(1, 13):
        ALL_PRODUCTS.add(i * j)

def make_distractors(a, b):
    """
    Generate 3 plausible wrong answers.
    Strategy: prefer other valid multiplication table products that are
    numerically close to the correct answer (mirrors the high-school
    near-miss error pattern). Avoid the correct answer itself.
    Falls back to ±2 offsets if not enough close products exist.
    """
    correct = a * b
    candidates = sorted(
        [p for p in ALL_PRODUCTS if p != correct],
        key=lambda p: abs(p - correct)
    )
    distractors = candidates[:3]
    # Ensure exactly 3
    while len(distractors) < 3:
        offset = len(distractors) + 1
        for sign in [1, -1]:
            val = correct + sign * offset
            if val > 0 and val != correct and val not in distractors:
                distractors.append(val)
                if len(distractors) == 3:
                    break
    return distractors[:3]

# ── Build card rows ───────────────────────────────────────────────────────────
# Current columns in cards_master (1-indexed):
#  A=id, B=deck, C=unit, D=question, E=answer,
#  F=distractor_1, G=distractor_2, H=distractor_3,
#  I=card_type, J=needs_image, K=tags, L=suspended, M=notes
# New columns to add: N=q_format, O=a_format, P=d_format

DECK    = "multiplication"
TAGS    = "elementary school math facts"

def make_id(a, b):
    return f"mult_{a}x{b}"

def make_question(a, b):
    # Uses \cdot for high school audiences (x is a variable)
    return f"{a} \\cdot {b}"

def make_answer(a, b):
    return str(a * b)

cards = []
for a in range(1, 13):
    for b in range(1, 13):
        d = make_distractors(a, b)
        cards.append({
            "id":           make_id(a, b),
            "deck":         DECK,
            "unit":         "",
            "question":     make_question(a, b),
            "answer":       make_answer(a, b),
            "distractor_1": str(d[0]),
            "distractor_2": str(d[1]),
            "distractor_3": str(d[2]),
            "card_type":    "cloze",
            "needs_image":  "FALSE",
            "tags":         TAGS,
            "suspended":    "FALSE",
            "notes":        get_note(a, b),
            "q_format":     "math",
            "a_format":     "math",
            "d_format":     "math",
        })

# ── Work on the spreadsheet ───────────────────────────────────────────────────
print("Opening cards_master tab…")
ws_cards = sh.worksheet("cards_master")
all_values = ws_cards.get_all_values()
header = all_values[0]

# ── Step 1: Add new format columns if missing ─────────────────────────────────
new_cols = ["q_format", "a_format", "d_format"]
added = []
for col_name in new_cols:
    if col_name not in header:
        header.append(col_name)
        added.append(col_name)

if added:
    print(f"Adding new header columns: {added}")
    # Write updated header row
    ws_cards.update("A1", [header], value_input_option="USER_ENTERED")
    time.sleep(1)

# Column index map (0-based)
col_idx = {name: i for i, name in enumerate(header)}
total_cols = len(header)

# ── Step 2: Backfill format columns for existing rows ─────────────────────────
# Existing rows (non-multiplication) get q_format/a_format/d_format = "math"
# since all current decks use the \( \) wrapping formula already.
# (You can change individual rows manually if a deck needs "text".)
if added:
    print("Backfilling format columns for existing rows…")
    existing_data_rows = all_values[1:]  # rows 2..N in sheet = index 0..N-2 here
    updates = []
    for row_i, row in enumerate(existing_data_rows):
        sheet_row = row_i + 2  # 1-based, +1 for header
        for col_name in added:
            ci = col_idx[col_name]
            cell = gspread.Cell(sheet_row, ci + 1, "math")
            updates.append(cell)
    if updates:
        batch_update(ws_cards, updates)
        time.sleep(1)
    print(f"  Backfilled {len(existing_data_rows)} existing rows.")

# ── Step 3: Append multiplication cards ──────────────────────────────────────
print("Appending 144 multiplication cards…")
ORDERED_COLS = [
    "id", "deck", "unit", "question", "answer",
    "distractor_1", "distractor_2", "distractor_3",
    "card_type", "needs_image", "tags", "suspended", "notes",
    "q_format", "a_format", "d_format",
]

rows_to_append = []
for card in cards:
    row = [""] * total_cols
    for col_name in ORDERED_COLS:
        if col_name in col_idx:
            row[col_idx[col_name]] = card.get(col_name, "")
    rows_to_append.append(row)

ws_cards.append_rows(rows_to_append, value_input_option="USER_ENTERED")
time.sleep(2)
print(f"  Appended {len(rows_to_append)} rows.")

# ── Step 4: Update the anki tab formula ───────────────────────────────────────
# New formula wraps question/answer in \( \) only when q_format/a_format = "math".
# Format columns: N=q_format (col 14), O=a_format (col 15)
# cards_master columns used: D=question(4), E=answer(5), N=q_format(14), O=a_format(15)
#
# Formula logic (per row n):
#   question part:
#     IF(cards_master!N{n}="math", "\("&cards_master!D{n}&"\)", cards_master!D{n})
#   answer part:
#     IF(cards_master!O{n}="math",
#        "{{c1::\("&cards_master!E{n}&"\)}}",
#        "{{c1::"&cards_master!E{n}&"}}")
#   full cloze cell:
#     = question_part & " = " & answer_part

print("Updating anki tab formulas…")
ws_anki = sh.worksheet("anki")
anki_values = ws_anki.get_all_values()
num_data_rows = len(all_values) + len(rows_to_append)  # header + old + new

# Build all formula cells (rows 2 through num_data_rows)
anki_updates = []

# Row 1: headers — keep as-is (they reference cards_master!A1, B1, D1)
# We only rebuild rows 2+

for row_i in range(1, num_data_rows):   # 0-based data index; row_i=0 → sheet row 2
    sheet_row = row_i + 1               # 1-based sheet row
    n = sheet_row                       # matches cards_master row number

    # Col A: id
    anki_updates.append(gspread.Cell(sheet_row, 1, f"=cards_master!A{n}"))
    # Col B: deck
    anki_updates.append(gspread.Cell(sheet_row, 2, f"=cards_master!B{n}"))
    # Col C: cloze text — format-aware
    q_part = (
        f'IF(cards_master!N{n}="math",'
        f'"\\("&cards_master!D{n}&"\\)",'
        f'cards_master!D{n})'
    )
    a_part = (
        f'IF(cards_master!O{n}="math",'
        f'"{{{{c1::\\("&cards_master!E{n}&"\\)}}}}",'
        f'"{{{{c1::"&cards_master!E{n}&"}}}}")'
    )
    formula = f"={q_part}&\" = \"&{a_part}"
    anki_updates.append(gspread.Cell(sheet_row, 3, formula))

# Send in chunks of 500 to avoid API limits
CHUNK = 500
for i in range(0, len(anki_updates), CHUNK):
    batch_update(ws_anki, anki_updates[i:i+CHUNK])
    time.sleep(1)
    print(f"  anki tab: updated rows up to {min(i+CHUNK, len(anki_updates))//3 + 1}…")

print("\n✅ Done!")
print(f"   • {len(added)} new columns added to cards_master: {added or 'none (already existed)'}")
print(f"   • 144 multiplication cards appended")
print(f"   • anki tab formulas updated to respect q_format / a_format")
print("\nNow run:  readsheet")
print("Check that the last rows are mult_12x12 and that column N shows 'math'.")