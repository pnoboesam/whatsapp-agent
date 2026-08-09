import os

import httpx
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

META_API_VERSION = "v25.0"

async def send_message(recipient: str, message: str):

    url = (
        f"https://graph.facebook.com/"
        f"{META_API_VERSION}/"
        f"{WHATSAPP_PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {
            "body": message
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json=payload,
        )

    print("Meta status:", response.status_code)
    print("Meta response:", response.text)

    return response.json()


if __name__ == "__main__":
    import asyncio

    asyncio.run(
        send_message(
            recipient="233553343550",
            message="Hello from my LangC WhatsApp agent"
        )
    )
