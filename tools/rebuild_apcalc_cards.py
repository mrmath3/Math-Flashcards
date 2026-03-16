from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = '11SzrA-74qZgYW9JXpe7LMXb8bDqxSQmL05X6VLYeLcA'
CREDS_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Exact cards from PDF, in order
# Columns: id, deck, unit, question, answer, d1, d2, d3, card_type, needs_image, tags, suspended, notes
# unit = first digit of lesson (e.g. 1-2 → unit 1)
# suspended: unit 1 = FALSE, units 2+ = TRUE

apcalc_cards = [
    # Page 1
    # 1-2
    ['APC-001', 'AP Calculus AB', '1', r'\lim_{x \to \#} f(x) = \frac{0}{0}:', 'factor, cancel, plug in', '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson2 limits', 'FALSE', ''],
    # 1-3
    ['APC-002', 'AP Calculus AB', '1', 'Horizontal Asymptote:', r'\lim_{x \to \pm\infty}', '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson3 limits', 'FALSE', ''],
    ['APC-003', 'AP Calculus AB', '1', r'\lim_{x \to \pm\infty} \frac{\text{TOP}}{\text{bot}} =', 'DNE', '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson3 limits', 'FALSE', ''],
    ['APC-004', 'AP Calculus AB', '1', r'\lim_{x \to \pm\infty} \frac{\text{top}}{\text{BOT}} =', '0', '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson3 limits', 'FALSE', ''],
    ['APC-005', 'AP Calculus AB', '1', r'\lim_{x \to \pm\infty} \frac{\text{top}}{\text{bot}} =', 'magic fraction', '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson3 limits', 'FALSE', ''],
    # 1-4
    ['APC-006', 'AP Calculus AB', '1', 'Types of discontinuities:', 'holes, gaps, VAs, ends', '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson4 continuity', 'FALSE', ''],
    ['APC-007', 'AP Calculus AB', '1', 'Continuity Test:', r'\lim_{x \to a^-} f(x) = \lim_{x \to a^+} f(x) = f(a)', '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson4 continuity', 'FALSE', ''],
    # 1-5
    ['APC-008', 'AP Calculus AB', '1', 'IVT:', 'If continuous, proves heights', '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson5 ivt', 'FALSE', ''],
    ['APC-009', 'AP Calculus AB', '1', 'EVT:', 'If continuous & closed, proves min & max', '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson5 evt', 'FALSE', ''],
    # 1-7
    ['APC-010', 'AP Calculus AB', '1', 'Not Differentiable:', 'discontinuous, sharp corners, vertical tangents', '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson7 differentiability', 'FALSE', ''],
    # 1-8
    ['APC-011', 'AP Calculus AB', '1', 'MVT:', 'If differentiable, proves slopes', '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson8 mvt', 'FALSE', ''],
    ['APC-012', 'AP Calculus AB', '1', 'MVT formula:', r"f'(c) = \frac{f(b) - f(a)}{b - a}", '', '', '', 'basic', 'FALSE', 'apcalc unit1 lesson8 mvt', 'FALSE', ''],
    # 2-1
    ['APC-013', 'AP Calculus AB', '2', r'\frac{d}{dx} ax^n \text{ (power house):}', r'n \cdot ax^{n-1}', '', '', '', 'basic', 'FALSE', 'apcalc unit2 lesson1 derivatives', 'TRUE', ''],
    # 2-3
    ['APC-014', 'AP Calculus AB', '2', 'Chain rule:', 'd-outer · d-inner', '', '', '', 'basic', 'FALSE', 'apcalc unit2 lesson3 chain-rule', 'TRUE', ''],
    # 2-5
    ['APC-015', 'AP Calculus AB', '2', r'\frac{d}{dx} e^x \text{ (e house):}', r'e^x', '', '', '', 'basic', 'FALSE', 'apcalc unit2 lesson5 derivatives', 'TRUE', ''],
    ['APC-016', 'AP Calculus AB', '2', r'\frac{d}{dx} \ln(x) \text{ (log house):}', r'\frac{1}{x}', '', '', '', 'basic', 'FALSE', 'apcalc unit2 lesson5 derivatives', 'TRUE', ''],
    # 2-6
    ['APC-017', 'AP Calculus AB', '2', r'\frac{d}{dx} \sin(x):', r'\cos(x)', '', '', '', 'basic', 'FALSE', 'apcalc unit2 lesson6 derivatives trig', 'TRUE', ''],
    ['APC-018', 'AP Calculus AB', '2', r'\frac{d}{dx} \cos(x):', r'-\sin(x)', '', '', '', 'basic', 'FALSE', 'apcalc unit2 lesson6 derivatives trig', 'TRUE', ''],
    ['APC-019', 'AP Calculus AB', '2', r'\frac{d}{dx} \tan(x):', r'\sec^2(x)', '', '', '', 'basic', 'FALSE', 'apcalc unit2 lesson6 derivatives trig', 'TRUE', ''],
    # 2-7
    ['APC-020', 'AP Calculus AB', '2', 'Differentiability Test:', r'\lim_{x \to a^-} f\'(x) = \lim_{x \to a^+} f\'(x) = f\'(a)', '', '', '', 'basic', 'FALSE', 'apcalc unit2 lesson7 differentiability', 'TRUE', ''],

    # Page 2
    # 2-8
    ['APC-021', 'AP Calculus AB', '2', r'\lim_{h \to 0}:', 'Hotbox', '', '', '', 'basic', 'FALSE', 'apcalc unit2 lesson8 limit-def', 'TRUE', ''],
    # 2-9
    ['APC-022', 'AP Calculus AB', '2', 'Product Rule:', '1d2 + 2d1', '', '', '', 'basic', 'FALSE', 'apcalc unit2 lesson9 product-rule', 'TRUE', ''],
    # 2-10
    ['APC-023', 'AP Calculus AB', '2', 'Quotient Rule:', r'\frac{\text{lo} \cdot \text{dhi} - \text{hi} \cdot \text{dlo}}{\text{lo}^2}', '', '', '', 'basic', 'FALSE', 'apcalc unit2 lesson10 quotient-rule', 'TRUE', ''],
    # 3-2
    ['APC-024', 'AP Calculus AB', '3', r'f\text{-inc:}', r"f' > 0", '', '', '', 'basic', 'FALSE', 'apcalc unit3 lesson2 increasing-decreasing', 'TRUE', ''],
    ['APC-025', 'AP Calculus AB', '3', r'f\text{-dec:}', r"f' < 0", '', '', '', 'basic', 'FALSE', 'apcalc unit3 lesson2 increasing-decreasing', 'TRUE', ''],
    ['APC-026', 'AP Calculus AB', '3', r'f\text{-CV:}', r"f' = 0 \text{ or } f' \text{ DNE}", '', '', '', 'basic', 'FALSE', 'apcalc unit3 lesson2 critical-values', 'TRUE', ''],
    # 3-3
    ['APC-027', 'AP Calculus AB', '3', r'f\text{-rel-ext:}', r"f' \text{ sign change}", '', '', '', 'basic', 'FALSE', 'apcalc unit3 lesson3 extrema', 'TRUE', ''],
    ['APC-028', 'AP Calculus AB', '3', r'f\text{-rel-max:}', r"f': + \to -", '', '', '', 'basic', 'FALSE', 'apcalc unit3 lesson3 extrema', 'TRUE', ''],
    ['APC-029', 'AP Calculus AB', '3', r'f\text{-rel-min:}', r"f': - \to +", '', '', '', 'basic', 'FALSE', 'apcalc unit3 lesson3 extrema', 'TRUE', ''],
    # 3-4
    ['APC-030', 'AP Calculus AB', '3', r'f\text{-con-up:}', r"f'' > 0", '', '', '', 'basic', 'FALSE', 'apcalc unit3 lesson4 concavity', 'TRUE', ''],
    ['APC-031', 'AP Calculus AB', '3', r'f\text{-con-down:}', r"f'' < 0", '', '', '', 'basic', 'FALSE', 'apcalc unit3 lesson4 concavity', 'TRUE', ''],
    ['APC-032', 'AP Calculus AB', '3', r'f\text{-IP:}', r"f'' \text{ sign change}", '', '', '', 'basic', 'FALSE', 'apcalc unit3 lesson4 inflection', 'TRUE', ''],
    # 4-1
    ['APC-033', 'AP Calculus AB', '4', 'tangent line equation:', r'y - \square = \square(x - \square)', '', '', '', 'basic', 'FALSE', 'apcalc unit4 lesson1 tangent-line', 'TRUE', ''],
    # 4-2
    ['APC-034', 'AP Calculus AB', '4', 'overestimate:', r"f'' < 0", '', '', '', 'basic', 'FALSE', 'apcalc unit4 lesson2 estimation', 'TRUE', ''],
    ['APC-035', 'AP Calculus AB', '4', 'underestimate:', r"f'' > 0", '', '', '', 'basic', 'FALSE', 'apcalc unit4 lesson2 estimation', 'TRUE', ''],
    # 4-5
    ['APC-036', 'AP Calculus AB', '4', r'\frac{d}{dx} y =', r"y'", '', '', '', 'basic', 'FALSE', 'apcalc unit4 lesson5 implicit', 'TRUE', ''],
    ['APC-037', 'AP Calculus AB', '4', r'\frac{d}{dx} y^2 =', r"2yy'", '', '', '', 'basic', 'FALSE', 'apcalc unit4 lesson5 implicit', 'TRUE', ''],
    ['APC-038', 'AP Calculus AB', '4', r'\frac{d}{dx} xy =', r"xy' + y", '', '', '', 'basic', 'FALSE', 'apcalc unit4 lesson5 implicit', 'TRUE', ''],
    # 4-7
    ['APC-039', 'AP Calculus AB', '4', r"A' =", r"A' = 2\pi r r' = C' r", '', '', '', 'basic', 'FALSE', 'apcalc unit4 lesson7 related-rates', 'TRUE', ''],
    ['APC-040', 'AP Calculus AB', '4', 'Circumference =', r'2\pi r', '', '', '', 'basic', 'FALSE', 'apcalc unit4 lesson7 related-rates', 'TRUE', ''],

    # Page 3
    # 4-7 (continued)
    ['APC-041', 'AP Calculus AB', '4', 'Area of Circle =', r'\pi r^2', '', '', '', 'basic', 'FALSE', 'apcalc unit4 lesson7 related-rates', 'TRUE', ''],
    # 4-9
    ['APC-042', 'AP Calculus AB', '4', 'Pythagorean Theorem:', r'a^2 + b^2 = c^2', '', '', '', 'basic', 'FALSE', 'apcalc unit4 lesson9 related-rates', 'TRUE', ''],
    # 5-1
    ['APC-043', 'AP Calculus AB', '5', r'\int \text{ power house:}', 'add one, divide down', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson1 integration', 'TRUE', ''],
    # 5-2
    ['APC-044', 'AP Calculus AB', '5', r'\text{For } \int \text{, always check:}', 'taxman', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson2 u-sub', 'TRUE', ''],
    # 5-4
    ['APC-045', 'AP Calculus AB', '5', r'\int x^{-1}:', r'\ln| \, |', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson4 integration', 'TRUE', ''],
    ['APC-046', 'AP Calculus AB', '5', r'\int e \text{ house:}', 'stays the same', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson4 integration', 'TRUE', ''],
    # 5-5
    ['APC-047', 'AP Calculus AB', '5', r'\int \sin:', r'-\cos', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson5 integration trig', 'TRUE', ''],
    ['APC-048', 'AP Calculus AB', '5', r'\int \cos:', r'\sin', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson5 integration trig', 'TRUE', ''],
    ['APC-049', 'AP Calculus AB', '5', r'\int \sec^2:', r'\tan', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson5 integration trig', 'TRUE', ''],
    # 5-6
    ['APC-050', 'AP Calculus AB', '5', r'\int_a^b f\'(x):', r'f(b) - f(a)', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson6 ftc', 'TRUE', ''],
    # 5-7
    ['APC-051', 'AP Calculus AB', '5', r'\int \text{ graph:}', 'area', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson7 definite-integral', 'TRUE', ''],
    # 5-8
    ['APC-052', 'AP Calculus AB', '5', r'\int \text{ piecewise:}', 'break at suspect', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson8 piecewise', 'TRUE', ''],
    # 5-9
    ['APC-053', 'AP Calculus AB', '5', r'\int_a^b \#:', r'(b - a) \cdot \#', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson9 properties', 'TRUE', ''],
    ['APC-054', 'AP Calculus AB', '5', r'\int_a^a f(x):', '0', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson9 properties', 'TRUE', ''],
    ['APC-055', 'AP Calculus AB', '5', r'\int k \cdot f(x):', r'k \cdot \int f(x)', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson9 properties', 'TRUE', ''],
    ['APC-056', 'AP Calculus AB', '5', r'\int f(x) + g(x):', r'\int f(x) + \int g(x)', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson9 properties', 'TRUE', ''],
    ['APC-057', 'AP Calculus AB', '5', r'\int_b^a f(x):', r'-\int_a^b f(x)', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson9 properties', 'TRUE', ''],
    ['APC-058', 'AP Calculus AB', '5', r'\int_a^c f(x) + \int_c^b f(x):', r'\int_a^b f(x)', '', '', '', 'basic', 'FALSE', 'apcalc unit5 lesson9 properties', 'TRUE', ''],
    # 6-2
    ['APC-059', 'AP Calculus AB', '6', '"particular solution":', 'separate, integrate, evaluate', '', '', '', 'basic', 'FALSE', 'apcalc unit6 lesson2 diff-eq', 'TRUE', ''],
    # 7-1
    ['APC-060', 'AP Calculus AB', '7', r'\frac{d}{dx} \text{(position):}', r'v', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson1 motion', 'TRUE', ''],

    # Page 4
    # 7-1 (continued)
    ['APC-061', 'AP Calculus AB', '7', r'\frac{d}{dx} \text{(velocity):}', r'a', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson1 motion', 'TRUE', ''],
    # 7-2
    ['APC-062', 'AP Calculus AB', '7', r'\int \text{ acceleration:}', r'v', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson2 motion', 'TRUE', ''],
    ['APC-063', 'AP Calculus AB', '7', r'\int \text{ velocity:}', 'pos', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson2 motion', 'TRUE', ''],
    ['APC-064', 'AP Calculus AB', '7', r'total change in position over [a, b]:', r'\int_a^b v', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson2 motion', 'TRUE', ''],
    ['APC-065', 'AP Calculus AB', '7', r'average velocity over [a, b]:', r'\frac{\int_a^b v}{b - a} \text{ or } \frac{\Delta \text{position}}{\Delta \text{time}}', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson2 motion', 'TRUE', ''],
    # 7-3
    ['APC-066', 'AP Calculus AB', '7', 'at rest:', r'v = 0', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson3 motion', 'TRUE', ''],
    ['APC-067', 'AP Calculus AB', '7', 'moving right / up:', r'v > 0', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson3 motion', 'TRUE', ''],
    ['APC-068', 'AP Calculus AB', '7', 'moving left / down:', r'v < 0', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson3 motion', 'TRUE', ''],
    ['APC-069', 'AP Calculus AB', '7', 'change in direction:', r'v \text{ sign change}', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson3 motion', 'TRUE', ''],
    # 7-4
    ['APC-070', 'AP Calculus AB', '7', 'end position:', r'\text{start} + \text{change}', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson4 motion', 'TRUE', ''],
    ['APC-071', 'AP Calculus AB', '7', 'values to check for max / min questions:', 'start, rel-exts, end', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson4 motion', 'TRUE', ''],
    # 7-5
    ['APC-072', 'AP Calculus AB', '7', 'speed:', r'|v(t)|', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson5 speed', 'TRUE', ''],
    ['APC-073', 'AP Calculus AB', '7', 'speed increasing:', r'v \text{ and } a \text{ same sign}', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson5 speed', 'TRUE', ''],
    ['APC-074', 'AP Calculus AB', '7', 'speed decreasing:', r'v \text{ and } a \text{ different signs}', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson5 speed', 'TRUE', ''],
    ['APC-075', 'AP Calculus AB', '7', r'total distance traveled over [a, b]:', r'\int_a^b |v|', '', '', '', 'basic', 'FALSE', 'apcalc unit7 lesson5 speed', 'TRUE', ''],
    # 8-1
    ['APC-076', 'AP Calculus AB', '8', r'\square \text{ increasing or decreasing?}', r'\text{Derivative of } \square', '', '', '', 'basic', 'FALSE', 'apcalc unit8 lesson1 rates', 'TRUE', ''],
    ['APC-077', 'AP Calculus AB', '8', 'rate:', r"f' \text{ (units / time)}", '', '', '', 'basic', 'FALSE', 'apcalc unit8 lesson1 rates', 'TRUE', ''],
    # 8-2
    ['APC-078', 'AP Calculus AB', '8', r'total change over [a, b]:', r"\int_a^b f' \text{ (units)}", '', '', '', 'basic', 'FALSE', 'apcalc unit8 lesson2 accumulation', 'TRUE', ''],
    # 8-3
    ['APC-079', 'AP Calculus AB', '8', 'final amount:', r'\text{start} + \text{change} = \text{end}', '', '', '', 'basic', 'FALSE', 'apcalc unit8 lesson3 accumulation', 'TRUE', ''],
    # 8-4
    ['APC-080', 'AP Calculus AB', '8', '(+) rate and (−) rate:', r'\text{total rate} = (+) - (-)', '', '', '', 'basic', 'FALSE', 'apcalc unit8 lesson4 rates', 'TRUE', ''],

    # Page 5
    # 8-4 (continued)
    ['APC-081', 'AP Calculus AB', '8', 'max/min:', r'\text{table with start} + \text{change} = \text{end}', '', '', '', 'basic', 'FALSE', 'apcalc unit8 lesson4 rates', 'TRUE', ''],
    # 9-1
    ['APC-082', 'AP Calculus AB', '9', r"Estimate f'(b):", r"\frac{f(c) - f(a)}{c - a}", '', '', '', 'basic', 'FALSE', 'apcalc unit9 lesson1 table', 'TRUE', ''],
    ['APC-083', 'AP Calculus AB', '9', r"What does \int_a^b f'(x)\,dx mean?", r'Total change in f in units from a to b units', '', '', '', 'basic', 'FALSE', 'apcalc unit9 lesson1 ftc', 'TRUE', ''],
    # 9-2
    ['APC-084', 'AP Calculus AB', '9', 'Left Riemann Sum:', r'(b - a) \cdot f(a) + (c - b) \cdot f(b)', '', '', '', 'basic', 'FALSE', 'apcalc unit9 lesson2 riemann', 'TRUE', ''],
    ['APC-085', 'AP Calculus AB', '9', 'Right Riemann Sum:', r'(b - a) \cdot f(b) + (c - b) \cdot f(c)', '', '', '', 'basic', 'FALSE', 'apcalc unit9 lesson2 riemann', 'TRUE', ''],
    ['APC-086', 'AP Calculus AB', '9', 'Midpoint Riemann Sum:', r'(c - a) \cdot f(b)', '', '', '', 'basic', 'FALSE', 'apcalc unit9 lesson2 riemann', 'TRUE', ''],
    # 9-3
    ['APC-087', 'AP Calculus AB', '9', 'Trapezoidal Riemann Sum:', r'(b - a) \cdot \text{avg}[f(a)\ \&\ f(b)] + (c - b) \cdot \text{avg}[f(b)\ \&\ f(c)]', '', '', '', 'basic', 'FALSE', 'apcalc unit9 lesson3 riemann', 'TRUE', ''],
    ['APC-088', 'AP Calculus AB', '9', r"What does \frac{1}{b-a} \int_a^b f'(x)\,dx mean?", r"Average f'(x) in units, from a to b units", '', '', '', 'basic', 'FALSE', 'apcalc unit9 lesson3 average', 'TRUE', ''],
    # 10-2
    ['APC-089', 'AP Calculus AB', '10', r'\frac{d}{dx} \int_{\#}^{x} f(t)\,dt =', r'f(x)', '', '', '', 'basic', 'FALSE', 'apcalc unit10 lesson2 ftc', 'TRUE', ''],
    ['APC-090', 'AP Calculus AB', '10', r'\frac{d}{dx} \int_{\#}^{x^2} f(t)\,dt =', r'f(x^2) \cdot 2x', '', '', '', 'basic', 'FALSE', 'apcalc unit10 lesson2 ftc', 'TRUE', ''],
    # 11-1
    ['APC-091', 'AP Calculus AB', '11', 'Area of the shaded region (left/right split):', r'\int_a^b \text{left} + \int_b^c \text{right}', '', '', '', 'basic', 'FALSE', 'apcalc unit11 lesson1 area', 'TRUE', ''],
    # 11-2
    ['APC-092', 'AP Calculus AB', '11', 'Area of the shaded region (top/bottom):', r'\int_a^b \text{top} - \text{bot}', '', '', '', 'basic', 'FALSE', 'apcalc unit11 lesson2 area', 'TRUE', ''],
    # 11-3
    ['APC-093', 'AP Calculus AB', '11', 'Volume of square cross section:', r'\int (\text{top} - \text{bot})^2', '', '', '', 'basic', 'FALSE', 'apcalc unit11 lesson3 volume', 'TRUE', ''],
    # 11-4
    ['APC-094', 'AP Calculus AB', '11', 'Volume rotated around x-axis:', r'\pi \int (\text{outer})^2 - (\text{inner})^2', '', '', '', 'basic', 'FALSE', 'apcalc unit11 lesson4 volume', 'TRUE', ''],
    # 11-5
    ['APC-095', 'AP Calculus AB', '11', r'Volume rotated around y = k:', r'\pi \int (\text{outer} - k)^2 - (\text{inner} - k)^2', '', '', '', 'basic', 'FALSE', 'apcalc unit11 lesson5 volume', 'TRUE', ''],
]

print(f"Total cards: {len(apcalc_cards)}")

# Step 1: Delete existing APC rows (rows 112-206 = 95 rows)
print("Deleting existing APC rows...")
sheet.batchUpdate(
    spreadsheetId=SPREADSHEET_ID,
    body={'requests': [{
        'deleteDimension': {
            'range': {
                'sheetId': 0,  # cards_master
                'dimension': 'ROWS',
                'startIndex': 111,  # 0-indexed, so row 112
                'endIndex': 206    # exclusive
            }
        }
    }]}
).execute()
print("  Deleted rows 112-206")

# Step 2: Append new cards
print("Appending new APC cards...")
result = sheet.values().append(
    spreadsheetId=SPREADSHEET_ID,
    range='cards_master!A:M',
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body={'values': apcalc_cards}
).execute()
print(f"  Added {result['updates']['updatedRows']} rows")

# Step 3: Rebuild anki tab (same formula pattern, rows 2-206)
print("Rebuilding anki tab...")
anki_rows = [['=cards_master!A1', '=cards_master!B1', '=cards_master!D1']]
for i in range(2, 207):
    formula = f'="\\("&cards_master!D{i}&"\\) = {{{{c1::\\("&cards_master!E{i}&"\\)}}}}"'
    anki_rows.append([f'=cards_master!A{i}', f'=cards_master!B{i}', formula])

sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range='anki!A:C').execute()
sheet.values().update(
    spreadsheetId=SPREADSHEET_ID,
    range='anki!A1',
    valueInputOption='USER_ENTERED',
    body={'values': anki_rows}
).execute()
print(f"  Rebuilt {len(anki_rows)} anki rows")

print("\nDone!")