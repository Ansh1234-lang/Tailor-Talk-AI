from calendar_utils import check_availability, book_event
from datetime import datetime, timedelta

# Set a test date (tomorrow)
date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

print("🔍 Checking availability...")
availability = check_availability(date)
print("✅ Availability result:", availability)

print("\n📅 Booking meeting...")
confirmation = book_event("TailorTalk Test Meeting", date, "15:00")
print("✅ Booking confirmation:", confirmation)
