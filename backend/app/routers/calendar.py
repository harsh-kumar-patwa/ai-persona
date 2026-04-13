from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.calendar_service import get_available_slots, book_slot, get_booking_link

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


class BookingRequest(BaseModel):
    slot_time: str
    name: str
    email: str
    notes: str = ""


@router.get("/slots")
async def get_slots(date_from: str = None, date_to: str = None):
    try:
        slots = await get_available_slots(date_from, date_to)
        return {"slots": slots}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch slots: {str(e)}")


@router.post("/book")
async def book(request: BookingRequest):
    try:
        result = await book_slot(
            slot_time=request.slot_time,
            name=request.name,
            email=request.email,
            notes=request.notes,
        )
        return {"booking": result, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Booking failed: {str(e)}")


@router.get("/link")
async def booking_link():
    return {"link": get_booking_link()}
