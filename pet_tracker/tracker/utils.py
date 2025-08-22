from datetime import datetime, date

def parse_dt(dt_str: str):
    try:
        return datetime.fromisoformat(dt_str)
    except Exception:
        return None

def summarize_today(activities, today=None):
    today = today or date.today()
    summary = {"walk_minutes": 0, "meals": 0, "meds": 0}
    todays = []

    for a in activities:
        dt = parse_dt(a.get("datetime", ""))
        if not dt:
            continue
        if dt.date() == today:
            todays.append(a)
            if a.get("type") == "walk":
                try:
                    summary["walk_minutes"] += int(a.get("amount", 0))
                except Exception:
                    pass
            elif a.get("type") == "meal":
                summary["meals"] += 1
            elif a.get("type") == "medication":
                summary["meds"] += 1
    return summary, todays
