import httpx
from datetime import datetime, timedelta
from app.config import CALCOM_API_KEY, CALCOM_EVENT_TYPE_ID, CALCOM_USERNAME

CALCOM_BASE_URL = "https://api.cal.com/v2"
CALCOM_HEADERS = {
    "Authorization": f"Bearer {CALCOM_API_KEY}",
    "cal-api-version": "2024-06-14",
    "Content-Type": "application/json",
}


async def get_available_slots(date_from: str = None, date_to: str = None) -> list[dict]:
    """Get available slots from Cal.com v2 API."""
    if not date_from:
        date_from = datetime.now().strftime("%Y-%m-%d")
    if not date_to:
        date_to = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CALCOM_BASE_URL}/slots/available",
            params={
                "startTime": f"{date_from}T00:00:00.000Z",
                "endTime": f"{date_to}T23:59:59.000Z",
                "eventTypeId": CALCOM_EVENT_TYPE_ID,
            },
            headers=CALCOM_HEADERS,
        )
        response.raise_for_status()
        data = response.json()

    slots = []
    slot_data = data.get("data", {}).get("slots", {})
    for date, time_slots in slot_data.items():
        for slot in time_slots:
            slots.append({
                "time": slot.get("time"),
                "date": date,
            })

    return slots


async def book_slot(
    slot_time: str,
    name: str,
    email: str,
    notes: str = "",
) -> dict:
    """Book a slot on Cal.com v2 API."""
    # Convert slot_time to UTC if it has a timezone offset
    try:
        dt = datetime.fromisoformat(slot_time.replace("Z", "+00:00"))
        utc_time = dt.astimezone(tz=None).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        # If it was already UTC-like, just normalize the format
        utc_time = dt.strftime("%Y-%m-%dT%H:%M:%S.000Z") if dt.tzname() == "UTC" else dt.astimezone(datetime.now().astimezone().tzinfo).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    except Exception:
        utc_time = slot_time

    # Find the closest matching UTC slot from Cal.com
    # This ensures we send an exact slot time that Cal.com recognizes
    try:
        date_str = slot_time[:10]
        available = await get_available_slots(date_from=date_str, date_to=date_str)
        # Try to match the requested time to an available slot
        from datetime import timezone as tz
        requested_dt = datetime.fromisoformat(slot_time.replace("Z", "+00:00"))
        best_slot = None
        min_diff = float("inf")
        for s in available:
            slot_dt = datetime.fromisoformat(s["time"].replace("Z", "+00:00"))
            diff = abs((requested_dt - slot_dt).total_seconds())
            if diff < min_diff:
                min_diff = diff
                best_slot = s["time"]
        if best_slot:
            utc_time = best_slot
    except Exception:
        pass

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CALCOM_BASE_URL}/bookings",
            headers=CALCOM_HEADERS,
            json={
                "eventTypeId": int(CALCOM_EVENT_TYPE_ID),
                "start": utc_time,
                "responses": {
                    "name": name,
                    "email": email,
                },
                "timeZone": "Asia/Kolkata",
                "language": "en",
                "metadata": {},
            },
        )
        response.raise_for_status()
        return response.json()


def get_booking_link() -> str:
    """Return the public Cal.com booking link."""
    if CALCOM_USERNAME:
        return f"https://cal.com/{CALCOM_USERNAME}/15min"
    return "https://cal.com"
