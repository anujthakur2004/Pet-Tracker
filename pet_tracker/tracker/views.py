from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import datetime
import json

from .storage import add_activity, get_activities, add_chat, get_chat
from .utils import summarize_today, parse_dt

def index(request):
    errors = []
    success = None

    # Handle success after redirect (PRG)
    if request.GET.get("success"):
        success = "Activity logged!"

    if request.method == "POST":
        pet = (request.POST.get("pet") or "").strip()
        type_ = (request.POST.get("type") or "").strip()
        amount = (request.POST.get("amount") or "").strip()
        dt_str = (request.POST.get("datetime") or "").strip() or datetime.now().strftime("%Y-%m-%dT%H:%M")

        if not pet:
            errors.append("Pet name is required.")
        if type_ not in {"walk", "meal", "medication"}:
            errors.append("Invalid activity type.")
        try:
            amt_val = int(amount)
            if amt_val <= 0:
                errors.append("Amount must be > 0.")
        except Exception:
            errors.append("Amount must be a number.")

        dt_val = parse_dt(dt_str)
        if not dt_val:
            errors.append("Invalid date/time.")
        elif dt_val > datetime.now():
            errors.append("Date/time cannot be in the future.")

        if not errors:
            add_activity({
                "pet": pet,
                "type": type_,
                "amount": amount,
                "datetime": dt_str,
            })
            return HttpResponseRedirect(reverse("index") + "?success=1")

    activities = get_activities()
    summary, todays = summarize_today(activities)

    return render(request, "tracker/index.html", {
        "errors": errors,
        "success": success,
        "summary": summary,
        "todays": todays,
    })

def summary_view(request):
    activities = get_activities()
    summary, todays = summarize_today(activities)
    return render(request, "tracker/summary.html", {"summary": summary, "todays": todays})

@require_http_methods(["POST"])
@csrf_exempt  # makes chatbot work without CSRF token hassle (safe for this demo)
def api_chat(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        data = request.POST

    user_text = (data.get("message") or "").strip()
    if not user_text:
        return JsonResponse({"ok": False, "error": "message required"}, status=400)

    add_chat({"role": "user", "text": user_text})

    acts = get_activities()
    summary, _ = summarize_today(acts)
    reply = None
    txt = user_text.lower()

    if "walk" in txt:
        reply = f"🐾 Today: {summary['walk_minutes']} minutes of walk."
    elif "meal" in txt or "food" in txt:
        reply = f"🍖 Meals today: {summary['meals']}."
    elif "med" in txt or "medicine" in txt:
        reply = f"💊 Medications: {summary['meds']}."

    if not reply:
        history = [m["text"] for m in get_chat() if m["role"] == "user"]
        if len(history) >= 2:
            reply = f"I remember you said: “{history[-2]}”."
        else:
            reply = "I'm here to track walks, meals & meds! Ask me anything."

    add_chat({"role": "bot", "text": reply})
    return JsonResponse({"ok": True, "reply": reply})
