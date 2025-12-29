from datetime import datetime, timedelta
from dateutil.parser import parse
import json
import re

# Load recalled batches database
with open("recalled_batches.json", "r") as f:
    RECALLED_DB = json.load(f)

def parse_date(text):
    try:
        date_patterns = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text)
        if date_patterns:
            return parse(date_patterns[0])
        return None
    except:
        return None

def check_expiry(expiry_date):
    today = datetime.now()
    if not expiry_date:
        return "unknown"
    if expiry_date < today:
        return "expired"
    if expiry_date <= today + timedelta(days=90):
        return "near_expiry"
    return "ok"

def check_recalled(medicine_name, batch_number):
    if not medicine_name or not batch_number:
        return None
    key = medicine_name.lower().strip()
    batches = RECALLED_DB.get(key, [])
    for b in batches:
        if b.get("batch", "").lower() == batch_number.lower():
            return b
    return None

def extract_batch(text):
    match = re.search(r"\b([A-Za-z]{1,5}-?\d{1,5})\b", text)
    return match.group(1) if match else ""

def normalize_medicine_name(text):
    text = text.lower().strip()
    text = re.sub(r"\b(tablet|capsule|syrup|cream|ointment|injection|ml|mg|exp|batch)\b", "", text)
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def get_bot_response(user_input):
    try:
        name = normalize_medicine_name(user_input)
        batch = extract_batch(user_input)
        expiry_date = parse_date(user_input)
        expiry_status = check_expiry(expiry_date)
        recalled = check_recalled(name, batch)

        if recalled:
            return f"⚠️ {name.title()} batch {batch} has been recalled!"
        elif expiry_status == "expired":
            return f"❌ {name.title()} batch {batch} is expired!"
        elif expiry_status == "near_expiry":
            return f"⚠️ {name.title()} batch {batch} is near expiry."
        else:
            return f"✅ {name.title()} batch {batch or 'N/A'} is safe."
    except Exception as e:
        return "⚠️ Bot encountered an error. Please try again."



