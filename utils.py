from datetime import datetime, timedelta
from dateutil.parser import parse
import json
import re

with open("recalled_batches.json", "r") as f:
    RECALLED_DB = json.load(f)

def parse_date(text):
    try:
        return parse(text, fuzzy=True)
    except:
        return None

def check_expiry(expiry_date):
    today = datetime.now()
    if expiry_date < today:
        return "expired"
    if expiry_date <= today + timedelta(days=90):
        return "near_expiry"
    return "ok"

def extract_batch(text):
    match = re.search(r"\b[A-Z]{1,4}-?\d{1,5}\b", text.upper())
    return match.group(0) if match else ""

def normalize_medicine_name(text):
    text = re.sub(r"(batch|expiry|exp|mg|ml|tablet|capsule)", "", text.lower())
    text = re.sub(r"[^a-z ]", "", text)
    return text.strip()

def check_recalled(medicine, batch):
    if not medicine or not batch:
        return None
    batches = RECALLED_DB.get(medicine, [])
    for b in batches:
        if b["batch"] == batch:
            return b
    return None









