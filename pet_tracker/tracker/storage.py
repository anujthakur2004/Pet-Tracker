from threading import Lock

_store = {
    "activities": [],  # list of dicts: {pet, type, amount, datetime}
    "chat": []         # list of dicts: {role: "user"/"bot", text: "..."}
}
_lock = Lock()

def add_activity(activity: dict):
    with _lock:
        _store["activities"].append(activity)

def get_activities():
    with _lock:
        return list(_store["activities"])

def add_chat(msg: dict):
    with _lock:
        _store["chat"].append(msg)

def get_chat():
    with _lock:
        return list(_store["chat"])
