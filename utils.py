from datetime import datetime, timedelta
from dateutil.parser import parse
import json

with open("recalled_batches.json") as f:
    RECALLS = json.load(f)

def check_expiry(date_str):
    try:
        date = parse(date_str)
        today = datetime.now()
        if date < today:
            return "expired"
        if date <= today + timedelta(days=90):
            return "near"
        return "safe"
    except:
        return None

def check_recall(med, batch):
    med = med.lower()
    if med in RECALLS:
        for r in RECALLS[med]:
            if r["batch"].lower() == batch.lower():
                return r["reason"]
    return None









