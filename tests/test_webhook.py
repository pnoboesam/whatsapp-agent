import hashlib
import hmac
import os
import requests
from dotenv import load_dotenv

load_dotenv()

secret = os.getenv("META_APP_SECRET")

body = b'''{
  "entry": [
    {
      "id": "770846489383893",
      "changes": [
        {
          "field": "messages",
          "value": {
            "contacts": [
              {
                "wa_id": "233553343550",
                "profile": {
                  "name": "MarketingIsPrince",
                  "username": "pnoboesam"
                },
                "user_id": "GH.1325970839515651"
              }
            ],
            "messages": [
              {
                "id": "48d33rda17",
                "from": "233553343550",
                "text": {
                  "body": "hi"
                },
                "type": "text",
                "timestamp": "1786480176",
                "from_user_id": "GH.1325970839515651"
              }
            ],
            "metadata": {
              "phone_number_id": "1069329939606586",
              "display_phone_number": "233269017360"
            },
            "messaging_product": "whatsapp"
          }
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}'''

signature = hmac.new(
    secret.encode("utf-8"),
    body,
    hashlib.sha256,
).hexdigest()

headers = {
    "X-Hub-Signature-256": f"sha256={signature}",
    "Content-Type": "application/json",
}

response = requests.post(
    "http://127.0.0.1:8000/api/v1/whatsapp/webhook",
    headers=headers,
    data=body,
)

print("Status:", response.status_code)
print("Response:", response.text)