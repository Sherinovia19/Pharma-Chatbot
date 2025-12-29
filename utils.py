import json
import re
from datetime import datetime, timedelta
from dateutil.parser import parse

# Load recalled batches
with open("recalled_batches.json", "r") as f:
    RECALLED_DB = json.load(f)

# Predefined storage guidance
STORAGE_GUIDANCE = {
    "vitamin d": "Store in a cool, dry place away from sunlight.",
    "paracetamol": "Keep below 25°C and avoid moisture.",
    "amoxicillin": "Store in a dry place, do not freeze.",
    "default": "Store in a cool, dry place away from sunlight."
}

def parse_date(text):
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    if dates:
        try:
            return parse(dates[0])
        except:
            return None
    try:
        return parse(text)
    except:
        return None

def check_expiry(expiry_date):
    today = datetime.now()
    if expiry_date < today:
        return "expired"
    if expiry_date <= today + timedelta(days=90):
        return "near_expiry"
    return "ok"

def check_recalled(name, batch):
    key = name.lower().strip()
    batches = RECALLED_DB.get(key, [])
    for b in batches:
        if b.get("batch", "").lower() == batch.lower():
            return b
    return None

def normalize_name(name):
    text = name.lower()
    text = re.sub(r"\b(tablet|capsule|syrup|cream|ointment|injection|ml|mg|exp|batch)\b", "", text)
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def get_bot_response(message):
    message = message.lower()
    
    # Check storage advice
    for med in STORAGE_GUIDANCE:
        if med in message:
            return STORAGE_GUIDANCE[med]
    
    # Check medicine, batch, expiry
    med_match = re.search(r"(check medicine: )([a-zA-Z0-9 ]+)", message)
    if med_match:
        med_name = normalize_name(med_match.group(2))
        batch_match = re.search(r"batch: ([a-zA-Z0-9-]+)", message)
        batch_number = batch_match.group(1) if batch_match else ""
        expiry_match = re.search(r"expiry: ([0-9-]+)", message)
        expiry_text = expiry_match.group(1) if expiry_match else ""
        expiry_date = parse_date(expiry_text)
        
        reply = f"Medicine: {med_name.title()}\n"
        
        if batch_number:
            reply += f"Batch: {batch_number}\n"
        if expiry_date:
            status = check_expiry(expiry_date)
            if status=="expired":
                reply += f"Status: ❌ Expired"
            elif status=="near_expiry":
                reply += f"Status: ⚠️ Near Expiry"
            else:
                reply += f"Status: ✅ Safe"
        else:
            reply += "Expiry: N/A"

        recalled = check_recalled(med_name, batch_number)
        if recalled:
            reply += f"\n⚠️ This batch has been recalled: {recalled.get('reason','Unknown')}"
        
        return reply
    
    # Default generic reply
    return "I'm here to help you with medicine expiry, batch recalls, and storage advice. Try typing 'Check medicine: Paracetamol, Batch: ABC-123, Expiry: 2025-12-29' or ask 'How should I store Vitamin D tablets?'"





