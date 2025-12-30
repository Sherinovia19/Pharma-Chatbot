from datetime import datetime

def check_expiry(date_str):
    try:
        expiry = datetime.strptime(date_str, "%d/%m/%Y").date()
        today = datetime.today().date()
        days_left = (expiry - today).days

        if days_left < 0:
            return "expired", abs(days_left)
        elif days_left <= 30:
            return "expiring_soon", days_left
        else:
            return "valid", days_left
    except:
        return "invalid", None
