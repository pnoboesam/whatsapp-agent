import hashlib
import hmac
import os
import requests
from dotenv import load_dotenv

load_dotenv()

secret = os.getenv("META_APP_SECRET")

body = b'''{
    "object": "whatsapp_business_account",
    "entry": [
        {
            "changes": [
                {
                    "value": {
                        "messages": [
                            {
                                "id": "test-message-123",
                                "from": "233555123456",
                                "type": "text",
                                "text": {
                                    "body": "Hello"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
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