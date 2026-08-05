import gspread
from google.oauth2.service_account import Credentials

from datetime import datetime
from app.schemas.lead import Lead

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file(
    "secrets/google-service-account.json",
    scopes=SCOPES,
)

client = gspread.authorize(creds)

SPREADSHEET_NAME = "LC EC WA Agent"
sheet = client.open(SPREADSHEET_NAME).sheet1

def append_lead(lead: Lead):
    sheet.append_row(
        [
            datetime.now().strftime("%d %b @ %I:%M %p"),
            lead.full_name,
            lead.phone_number,
            lead.location,
            lead.concern,
            lead.wa_number,
            lead.source,
            lead.issue_category,
            lead.remarks,
        ]
    )

    print('Lead added')


if __name__ == "__main__":
    lead = Lead(
        full_name="Prince",
        phone_number="0240000000",
        location="East Legon",
        concern="Botox treatment",
        wa_number="0240000000",
        issue_category="Cosmetic Skin Treatment",
        remarks="Interested in Botox consultation",
        conversation_summary="User is interested in Botox treatment."
    )

    append_lead(lead)
