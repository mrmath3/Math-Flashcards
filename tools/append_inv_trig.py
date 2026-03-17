import json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS_FILE = '/Users/mrmath3/Documents/GitHub/Math-Flashcards/tools/credentials.json'
SHEET_ID = '11SzrA-74qZgYW9JXpe7LMXb8bDqxSQmL05X6VLYeLcA'

creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)
ws = sh.worksheet('cards_master')

DECK = 'inverse trig values radians'
CARD_TYPE = 'cloze'
NEEDS_IMAGE = 'FALSE'
TAGS = 'trig'
SUSPENDED = 'FALSE'
NOTES = ''
Q_FMT = 'math'
A_FMT = 'math'
D_FMT = 'math'

# Each row: [id, deck, unit, question, answer, d1, d2, d3, card_type, needs_image, tags, suspended, notes, q_fmt, a_fmt, d_fmt]
rows = [
    # sin^-1 cards (Q1-Q9 from PDF)
    ['inv_sin_01', DECK, '', '\\sin^{-1}(-1)',         '-\\frac{\\pi}{2}',     '-\\frac{3\\pi}{2}', '\\frac{\\pi}{2}',      '\\frac{3\\pi}{2}',    CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_sin_02', DECK, '', '\\sin^{-1}\\left(-\\frac{\\sqrt3}{2}\\right)', '-\\frac{\\pi}{3}', '-\\frac{\\pi}{6}', '\\frac{\\pi}{3}',    '\\frac{5\\pi}{3}', CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_sin_03', DECK, '', '\\sin^{-1}\\left(-\\frac{\\sqrt2}{2}\\right)', '-\\frac{\\pi}{4}', '\\frac{3\\pi}{4}', '\\frac{\\pi}{4}',    '\\frac{7\\pi}{4}', CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_sin_04', DECK, '', '\\sin^{-1}\\left(-\\frac{1}{2}\\right)',        '-\\frac{\\pi}{6}', '-\\frac{\\pi}{3}', '\\frac{\\pi}{6}',    '\\frac{2\\pi}{3}', CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_sin_05', DECK, '', '\\sin^{-1}(0)',           '0',                    '\\frac{\\pi}{2}',  '-\\frac{\\pi}{4}', '\\frac{\\pi}{4}',     CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_sin_06', DECK, '', '\\sin^{-1}\\left(\\frac{1}{2}\\right)',         '\\frac{\\pi}{6}',  '\\frac{\\pi}{3}',  '-\\frac{\\pi}{6}',    '-\\frac{\\pi}{3}', CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_sin_07', DECK, '', '\\sin^{-1}\\left(\\frac{\\sqrt2}{2}\\right)',   '\\frac{\\pi}{4}',  '\\frac{\\pi}{2}',  '-\\frac{\\pi}{4}',    '-\\frac{\\pi}{2}', CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_sin_08', DECK, '', '\\sin^{-1}\\left(\\frac{\\sqrt3}{2}\\right)',   '\\frac{\\pi}{3}',  '\\frac{\\pi}{6}',  '-\\frac{\\pi}{3}',    '-\\frac{\\pi}{6}', CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_sin_09', DECK, '', '\\sin^{-1}(1)',            '\\frac{\\pi}{2}',     '\\frac{\\pi}{4}',  '0',               '-\\frac{\\pi}{2}',     CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],

    # cos^-1 cards (Q10-Q18 from PDF)
    ['inv_cos_01', DECK, '', '\\cos^{-1}(-1)',          '\\pi',                 '\\frac{\\pi}{2}',  '-\\pi',           '-\\frac{\\pi}{2}',     CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_cos_02', DECK, '', '\\cos^{-1}\\left(-\\frac{\\sqrt3}{2}\\right)', '\\frac{5\\pi}{6}', '-\\frac{\\pi}{3}', '\\frac{\\pi}{3}',    '\\frac{2\\pi}{3}', CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_cos_03', DECK, '', '\\cos^{-1}\\left(-\\frac{\\sqrt2}{2}\\right)', '\\frac{3\\pi}{4}', '-\\frac{\\pi}{4}', '\\frac{5\\pi}{4}',   '\\frac{\\pi}{4}',  CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_cos_04', DECK, '', '\\cos^{-1}\\left(-\\frac{1}{2}\\right)',        '\\frac{2\\pi}{3}', '-\\frac{\\pi}{6}', '\\frac{\\pi}{6}',    '\\frac{5\\pi}{6}', CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_cos_05', DECK, '', '\\cos^{-1}(0)',            '\\frac{\\pi}{2}',     '\\frac{\\pi}{4}',  '0',               '-\\frac{\\pi}{2}',     CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_cos_06', DECK, '', '\\cos^{-1}\\left(\\frac{1}{2}\\right)',         '\\frac{\\pi}{3}',  '-\\frac{\\pi}{3}', '-\\frac{\\pi}{6}',    '\\frac{\\pi}{6}',  CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_cos_07', DECK, '', '\\cos^{-1}\\left(\\frac{\\sqrt2}{2}\\right)',   '\\frac{\\pi}{4}',  '-\\frac{\\pi}{4}', '-\\frac{\\pi}{2}',    '\\frac{\\pi}{2}',  CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_cos_08', DECK, '', '\\cos^{-1}\\left(\\frac{\\sqrt3}{2}\\right)',   '\\frac{\\pi}{6}',  '\\frac{\\pi}{3}',  '-\\frac{\\pi}{3}',    '-\\frac{\\pi}{6}', CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_cos_09', DECK, '', '\\cos^{-1}(1)',            '0',                    '\\frac{\\pi}{4}',  '\\frac{\\pi}{2}',  '-\\frac{\\pi}{2}',     CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],

    # tan^-1 cards (Q19-Q25 from PDF)
    ['inv_tan_01', DECK, '', '\\tan^{-1}(-\\sqrt3)',     '-\\frac{\\pi}{3}',    '\\frac{\\pi}{3}',   '-\\frac{\\pi}{6}', '\\frac{\\pi}{6}',    CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_tan_02', DECK, '', '\\tan^{-1}(-1)',           '-\\frac{\\pi}{4}',    '\\frac{\\pi}{4}',   '-\\frac{\\pi}{2}', '\\frac{\\pi}{2}',    CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_tan_03', DECK, '', '\\tan^{-1}\\left(-\\frac{\\sqrt3}{3}\\right)',   '-\\frac{\\pi}{6}',   '\\frac{\\pi}{3}',   '\\frac{\\pi}{6}',   '-\\frac{\\pi}{3}', CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_tan_04', DECK, '', '\\tan^{-1}(0)',            '0',                    '-\\frac{\\pi}{2}',  '\\pi',             '\\frac{\\pi}{2}',     CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_tan_05', DECK, '', '\\tan^{-1}\\left(\\frac{\\sqrt3}{3}\\right)',    '\\frac{\\pi}{6}',    '-\\frac{\\pi}{6}',  '-\\frac{\\pi}{3}',   '\\frac{\\pi}{3}',  CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_tan_06', DECK, '', '\\tan^{-1}(1)',            '\\frac{\\pi}{4}',     '-\\frac{\\pi}{2}',  '-\\frac{\\pi}{4}', '\\frac{\\pi}{2}',    CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
    ['inv_tan_07', DECK, '', '\\tan^{-1}(\\sqrt3)',      '\\frac{\\pi}{3}',     '-\\frac{\\pi}{3}',  '\\frac{\\pi}{6}',  '-\\frac{\\pi}{6}',   CARD_TYPE, NEEDS_IMAGE, TAGS, SUSPENDED, NOTES, Q_FMT, A_FMT, D_FMT],
]

ws.append_rows(rows, value_input_option='RAW')
print(f"Successfully appended {len(rows)} rows.")
