import requests
import time
from dotenv import load_dotenv
import os
import csv
import random
from datetime import datetime

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = "https://www.wasenderapi.com/api/send-message"

# Files
NUMBER_FILE = "number.txt"
MESSAGE_FILE = "comment.txt"
SENT_FILE = "sent_numbers.csv"      # Persistent storage of sent numbers
LOG_FILE = "send_log.csv"           # Log with timestamp + response

# Your single clickable link
SINGLE_LINK = "https://1brl.now"

# Load numbers to send (UTF-8)
with open(NUMBER_FILE, "r", encoding="utf-8") as f:
    all_numbers = [line.strip() for line in f if line.strip()]

# Load message template (UTF-8)
with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
    message_text = f.read().strip()  # Use {link} as placeholder if desired

# Load sent numbers
sent_numbers = set()
if os.path.exists(SENT_FILE):
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                sent_numbers.add(row[0])

# Prepare numbers to send
numbers_to_send = [num for num in all_numbers if num not in sent_numbers]

print(f"Total numbers loaded: {len(all_numbers)}")
print(f"Numbers to send: {len(numbers_to_send)}")

# Ensure log file exists and has header
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "number", "status", "api_response"])

for number in numbers_to_send:
    # Replace placeholder {link} with single link
    text_to_send = message_text.replace("{link}", SINGLE_LINK)

    payload = {
        "to": number,
        "text": text_to_send
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=30
        )
        result = response.json()
        print(f"{number} -> {result}")

        # Determine status
        status = "success" if result.get("success") or result.get("status") == "sent" else "failed"

        # Log to CSV
        with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), number, status, str(result)])

        # If success, save number to sent file
        if status == "success":
            sent_numbers.add(number)
            with open(SENT_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([number])

    except Exception as e:
        print(f"Error sending to {number}: {e}")
        # Log exception as failed
        with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), number, "error", str(e)])

    # Wait 2 minutes + small random variation
    time.sleep(120 + random.uniform(1, 10))
