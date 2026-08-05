from langchain.tools import tool
from app.schemas.lead import Lead
from app.services.google_sheets import append_lead

@tool(args_schema=Lead)
def append_lead_details(**kwargs):
    """
    Save a lead to Google Sheets
    """
    
    lead = Lead(**kwargs)
    append_lead(lead)

    return "Lead added successfully."