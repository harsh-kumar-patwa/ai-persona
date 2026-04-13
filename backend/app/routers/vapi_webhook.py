"""Webhook endpoint for Vapi voice agent function calls."""
import json
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Request
from app.services.rag_service import retrieve_context
from app.services.calendar_service import get_available_slots, book_slot

router = APIRouter(prefix="/api/vapi", tags=["vapi"])

IST = timezone(timedelta(hours=5, minutes=30))


def _format_slot_time(iso_time: str) -> str:
    """Convert ISO time to a human-readable IST format for voice."""
    try:
        dt = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
        dt_ist = dt.astimezone(IST)
        return dt_ist.strftime("%A, %B %d at %I:%M %p IST")
    except Exception:
        return iso_time


async def _handle_function(fn_name: str, fn_params: dict) -> str:
    """Execute a function call and return the result string."""
    if fn_name == "getPersonInfo":
        query = fn_params.get("query", "")
        context = retrieve_context(query, clean=True)
        if len(context) > 2000:
            context = context[:2000]
        return context

    elif fn_name == "getAvailableSlots":
        try:
            # Always use real current dates regardless of what the LLM sends
            now = datetime.now(IST)
            date_from = now.strftime("%Y-%m-%d")
            date_to = (now + timedelta(days=7)).strftime("%Y-%m-%d")
            slots = await get_available_slots(
                date_from=date_from,
                date_to=date_to,
            )
            if not slots:
                return "No available slots found in the next 7 days."
            formatted = [_format_slot_time(s["time"]) for s in slots[:5]]
            return f"Today is {now.strftime('%A, %B %d, %Y')}. Here are the next available slots: {'; '.join(formatted)}. Would any of these work for you?"
        except Exception as e:
            return "I'm having trouble checking the calendar right now. Please try again."

    elif fn_name == "bookMeeting":
        try:
            result = await book_slot(
                slot_time=fn_params["slot_time"],
                name=fn_params["name"],
                email=fn_params["email"],
                notes=fn_params.get("notes", "Booked via AI voice agent"),
            )
            formatted_time = _format_slot_time(fn_params["slot_time"])
            return f"Meeting booked successfully for {fn_params['name']} on {formatted_time}. A confirmation will be sent to {fn_params['email']}."
        except Exception as e:
            return f"Sorry, I couldn't book that slot. Could you try a different time?"

    return "Unknown function."


@router.post("/webhook")
async def vapi_webhook(request: Request):
    """Handle Vapi server messages (function calls from the voice agent)."""
    body = await request.json()
    message = body.get("message", {})
    msg_type = message.get("type")

    # Vapi sends "tool-calls" with a list of tool calls
    if msg_type == "tool-calls":
        tool_calls = message.get("toolCallList", [])
        results = []
        for tool_call in tool_calls:
            tool_call_id = tool_call.get("id", "")
            function = tool_call.get("function", {})
            fn_name = function.get("name", "")
            # arguments come as a JSON string
            args_str = function.get("arguments", "{}")
            try:
                fn_params = json.loads(args_str) if isinstance(args_str, str) else args_str
            except json.JSONDecodeError:
                fn_params = {}

            result = await _handle_function(fn_name, fn_params)
            results.append({
                "toolCallId": tool_call_id,
                "result": result,
            })

        return {"results": results}

    # Legacy format: "function-call" (keep for backwards compatibility)
    if msg_type == "function-call":
        function_call = message.get("functionCall", {})
        fn_name = function_call.get("name", "")
        fn_params = function_call.get("parameters", {})
        result = await _handle_function(fn_name, fn_params)
        return {"result": result}

    return {"result": "OK"}
