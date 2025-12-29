from datetime import datetime, timedelta
from dateutil.parser import parse
import json, re

with open("recalled_batches.json", "r") as f:
    RECALLED_DB = json.load(f)

def parse_date(text):
    date_patterns = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text)
    if date_patterns:
        try: return parse(date_patterns[0])
        except: return None
    try: return parse(text)
    except: return None

def check_expiry(expiry_date):
    today = datetime.now()
    if expiry_date < today: return "expired"
    if expiry_date <= today + timedelta(days=90): return "near_expiry"
    return "ok"

def check_recalled(medicine_name, batch_number):
    if not medicine_name: return None
    key = medicine_name.lower().strip()
    batches = RECALLED_DB.get(key, [])
    for b in batches:
        if b.get("batch","").lower() == batch_number.lower(): return b
    return None

def extract_batch(text):
    match = re.search(r"\b([A-Za-z]{1,5}-?\d{1,5})\b", text)
    return match.group(1) if match else ""

def normalize_medicine_name(text):
    text = text.lower().strip()
    text = re.sub(r"\b(tablet|capsule|syrup|cream|ointment|injection|ml|mg|exp|batch)\b","",text)
    text = re.sub(r"[^a-z0-9 ]"," ",text)
    text = re.sub(r"\s+"," ",text).strip()
    return text

def get_bot_response(text):
    med_name = normalize_medicine_name(text)
    batch = extract_batch(text)
    expiry_date = parse_date(text)

    recall = check_recalled(med_name, batch)
    if recall:
        return f"❌ ALERT! {med_name.title()} batch {batch} has been recalled due to {recall['reason']}."

    if expiry_date:
        status = check_expiry(expiry_date)
        if status == "expired":
            return f"❌ {med_name.title()} is expired as of {expiry_date.date()}."
        elif status == "near_expiry":
            return f"⚠️ {med_name.title()} will expire soon on {expiry_date.date()}."
        else:
            return f"✅ {med_name.title()} is safe to use until {expiry_date.date()}."

    if "store" in text.lower():
        return f"🌡️ Store {med_name.title()} in a cool, dry place away from sunlight."

    return f"💡 I can check expiry, batch recalls, or storage info for {med_name.title()}."







