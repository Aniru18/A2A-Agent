from typing import Dict
from datetime import datetime

# ---------------------------------------
# In-memory Court Schedule (Dummy Data)
# ---------------------------------------

# Mapping:
# date (YYYY-MM-DD) -> { time_slot (HH:MM) -> status }
# status: "available" or reservation_name (means booked)

COURT_SCHEDULE: Dict[str, Dict[str, str]] = {
    "2025-11-10": {
        "08:00": "available",
        "09:00": "available",
        "10:00": "available",
    },
    "2025-11-11": {
        "08:00": "available",
        "09:00": "available",
        "10:00": "booked",   # Already booked by someone (dummy)
        "11:00": "available",
    },
    "2025-11-12": {
        "08:00": "available",
        "09:00": "available",
        "10:00": "available",
    },
}


def generate_court_schedule():
    """Dummy initializer (kept for compatibility)."""
    print("Court schedule initialized with fixed test dates and times.")


# Initialize dummy schedule
generate_court_schedule()


# ---------------------------------------
# List Availability
# ---------------------------------------

def list_court_availabilities(date: str) -> dict:
    """
    Lists available and booked time slots for a given date.
    """

    if date not in COURT_SCHEDULE:
        return {
            "status": "error",
            "message": f"No schedule found for {date}. Try another date.",
            "schedule": {},
        }

    daily_schedule = COURT_SCHEDULE[date]

    available_slots = [
        time for time, status in daily_schedule.items()
        if status == "available"
    ]

    booked_slots = {
        time: status
        for time, status in daily_schedule.items()
        if status != "available"
    }

    return {
        "status": "success",
        "message": f"Schedule for {date}.",
        "available_slots": available_slots,
        "booked_slots": booked_slots,
    }


# ---------------------------------------
# Book Court
# ---------------------------------------

def book_badminton_court(
    date: str,
    start_time: str,
    end_time: str,
    reservation_name: str
) -> dict:
    """
    Books a single-hour badminton court slot.
    """

    if date not in COURT_SCHEDULE:
        return {
            "status": "error",
            "message": f"No schedule available for {date}.",
        }

    if start_time not in COURT_SCHEDULE[date]:
        return {
            "status": "error",
            "message": f"Invalid time slot. Available slots are: {list(COURT_SCHEDULE[date].keys())}",
        }

    if COURT_SCHEDULE[date][start_time] != "available":
        return {
            "status": "error",
            "message": f"Slot {start_time} on {date} is already booked by {COURT_SCHEDULE[date][start_time]}.",
        }

    # Perform booking
    COURT_SCHEDULE[date][start_time] = reservation_name

    return {
        "status": "success",
        "message": f"Booking confirmed for {reservation_name} on {date} at {start_time}.",
    }