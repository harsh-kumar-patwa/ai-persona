"""Set up the Vapi voice assistant with the correct configuration."""
import os
import sys
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.config import VAPI_API_KEY

VAPI_BASE_URL = "https://api.vapi.ai"


def create_assistant(server_url: str, persona_name: str):
    """Create a Vapi assistant configured for the AI persona."""

    assistant_config = {
        "name": f"{persona_name} AI Persona",
        "model": {
            "provider": "openai",
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": f"""You are an AI representative for {persona_name}. You are answering a phone call on their behalf.

Your behavior:
- Introduce yourself: "Hi, I'm {persona_name}'s AI representative. I can answer questions about their background, skills, and experience, and help schedule an interview."
- Be conversational, professional, and confident
- Answer questions about their background using the getPersonInfo function
- When asked about scheduling, use getAvailableSlots to check availability
- When the caller wants to book, collect their name, email, and preferred time, then use bookMeeting
- If you don't have information, say so honestly
- Keep responses concise — this is a phone call, not an essay
- Handle interruptions gracefully

Important: Always use getPersonInfo to retrieve factual information. Do not make up details.""",
                }
            ],
            "functions": [
                {
                    "name": "getPersonInfo",
                    "description": "Retrieve information about the person's background, skills, experience, or projects",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The question or topic to look up",
                            }
                        },
                        "required": ["query"],
                    },
                },
                {
                    "name": "getAvailableSlots",
                    "description": "Get available meeting slots for the next 7 days",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "date_from": {
                                "type": "string",
                                "description": "Start date in YYYY-MM-DD format",
                            },
                            "date_to": {
                                "type": "string",
                                "description": "End date in YYYY-MM-DD format",
                            },
                        },
                    },
                },
                {
                    "name": "bookMeeting",
                    "description": "Book a meeting at a specific time slot",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "slot_time": {
                                "type": "string",
                                "description": "ISO datetime for the meeting slot",
                            },
                            "name": {
                                "type": "string",
                                "description": "Guest's full name",
                            },
                            "email": {
                                "type": "string",
                                "description": "Guest's email address",
                            },
                            "notes": {
                                "type": "string",
                                "description": "Optional notes for the meeting",
                            },
                        },
                        "required": ["slot_time", "name", "email"],
                    },
                },
            ],
        },
        "voice": {
            "provider": "11labs",
            "voiceId": "bIHbv24MWmeRgasZH58o",  # Will — professional male voice
        },
        "firstMessage": f"Hi there! I'm {persona_name}'s AI representative. I can tell you about their background, skills, and experience, or help you schedule an interview. What would you like to know?",
        "serverUrl": server_url,
        "endCallFunctionEnabled": True,
        "silenceTimeoutSeconds": 30,
        "maxDurationSeconds": 600,
        "backgroundSound": "off",
        "responseDelaySeconds": 0.5,
    }

    response = requests.post(
        f"{VAPI_BASE_URL}/assistant",
        headers={
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json",
        },
        json=assistant_config,
    )
    response.raise_for_status()
    assistant = response.json()
    print(f"Assistant created: {assistant['id']}")
    return assistant


def create_phone_number(assistant_id: str):
    """Purchase and assign a Vapi phone number to the assistant."""
    response = requests.post(
        f"{VAPI_BASE_URL}/phone-number",
        headers={
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "provider": "vapi",
            "assistantId": assistant_id,
        },
    )
    response.raise_for_status()
    phone = response.json()
    print(f"Phone number assigned: {phone.get('number', phone.get('id'))}")
    return phone


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python setup_vapi.py <server_url> <persona_name>")
        print("Example: python setup_vapi.py https://your-api.railway.app Harsh")
        sys.exit(1)

    server_url = sys.argv[1]
    persona_name = sys.argv[2]

    print(f"Setting up Vapi assistant for {persona_name}...")
    assistant = create_assistant(f"{server_url}/api/vapi/webhook", persona_name)

    print("Acquiring phone number...")
    phone = create_phone_number(assistant["id"])

    print("\n=== Setup Complete ===")
    print(f"Assistant ID: {assistant['id']}")
    print(f"Phone Number: {phone.get('number', 'Check Vapi dashboard')}")
    print(f"Server URL: {server_url}/api/vapi/webhook")
