# utils.py
from datetime import datetime, timedelta
from dateutil.parser import parse
import json
import re

# Load recalled batches database
with open("recalled_batches.json", "r") as f:
    RECALLED_DB = json.load(f)

def parse_date(text):
    """
    Try to parse a date from text.
    Returns datetime object or None if not found.
    """
    # Find all date-like patterns
    date_patterns = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text)
    if date_patterns:
        try:
            return parse(date_patterns[0])
        except:
            return None

    # fallback: try parsing anything with dateutil
    try:
        return parse(text, dayfirst=False, yearfirst=True)
    except:
        return None

def check_expiry(expiry_date):
    """
    Check if the product is expired or near expiry.
    Returns: 'expired', 'near_expiry', 'ok'
    """
    today = datetime.now()
    if expiry_date < today:
        return "expired"
    if expiry_date <= today + timedelta(days=90):
        return "near_expiry"
    return "ok"

def check_recalled(medicine_name, batch_number):
    """
    Check recalled database for a given medicine and batch.
    Returns batch info dict or None
    """
    if not medicine_name:
        return None
    key = medicine_name.lower().strip()
    batches = RECALLED_DB.get(key, [])
    for b in batches:
        if b.get("batch", "").lower() == batch_number.lower():
            return b
    return None

def extract_batch(text):
    """
    Extract a batch number from text.
    Batch assumed to be alphanumeric and may contain dashes.
    """
    # Look for patterns like PX-123, AMX-55, IB-789
    match = re.search(r"\b([A-Za-z]{1,5}-?\d{1,5})\b", text)
    return match.group(1) if match else ""

def normalize_medicine_name(text):
    """
    Extract medicine name from text and clean it.
    """
    text = text.lower().strip()
    # Remove common words like tablet, syrup, mg, ml, etc.
    text = re.sub(r"\b(tablet|capsule|syrup|cream|ointment|injection|ml|mg|exp|batch)\b", "", text)
    # Remove non-alphanumeric characters
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
