import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
CREDS_FILE = "tools/credentials.json"
SHEET_ID = "11SzrA-74qZgYW9JXpe7LMXb8bDqxSQmL05X6VLYeLcA"

creds = service_account.Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range="cards_master!A1:G3"
).execute()

rows = result.get("values", [])
for row in rows:
    print(row)

print("\n✅ Connection successful!")
