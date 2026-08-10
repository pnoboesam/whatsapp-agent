import os
import asyncio
import logging
import httpx
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504,}

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

    timeout = httpx.Timeout(10.0)

    async with httpx.AsyncClient(timeout=timeout) as client:

        for attempt in range(3):
            try:
                response = await client.post(
                    url,
                    headers=headers,
                    json=payload,
                )

                if response.status_code not in RETRYABLE_STATUS_CODES:
                    response.raise_for_status()
                    return response.json()

                logger.warning(
                    "Retryable WhatsApp API error: " \
                    "status=%s attempt=%s",
                    response.status_code,
                    attempt + 1,
                )

            except httpx.TimeoutException:
                logger.warning(
                    "WhatsApp API timeout: attempt=%s",
                    attempt + 1,
                )

            except httpx.RequestError as exc:
                logger.warning(
                    "WhatsApp API request error: "
                    "attempt=%s error=%s",
                    attempt + 1,
                    exc,
                )

            if attempt < 2:
                await asyncio.sleep(2 ** attempt)

    raise RuntimeError("Failed to send WhatsApp message after retries")