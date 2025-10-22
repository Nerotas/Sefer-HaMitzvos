#!/usr/bin/env python3
"""
Consent capture Lambda for WhatsApp Daily Mitzvah
- Handles Twilio inbound webhooks (JOIN/STOP) for WhatsApp
- Handles simple web form/JSON opt-in submissions
- Stores consent in DynamoDB table defined by SUBSCRIBERS_TABLE
"""

import json
import logging
import os
from datetime import datetime, timezone
from urllib.parse import parse_qs

import importlib

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _strip_channel_prefix(phone: str) -> str:
    if not phone:
        return phone
    for pref in ("whatsapp:", "tel:", "sms:"):
        if phone.startswith(pref):
            return phone[len(pref):]
    return phone


def _get_table():
    table_name = os.environ.get("SUBSCRIBERS_TABLE")
    if not table_name:
        raise RuntimeError("SUBSCRIBERS_TABLE env var is required")
    # Dynamically import boto3 to avoid local lint errors when not installed
    boto3 = importlib.import_module("boto3")
    ddb = boto3.resource("dynamodb")
    return ddb.Table(table_name)


def _respond(status=200, body=None, headers=None, is_xml=False):
    hdrs = {"Content-Type": "application/xml" if is_xml else "application/json"}
    if headers:
        hdrs.update(headers)
    return {
        "statusCode": status,
        "headers": hdrs,
        "body": body if is_xml else json.dumps(body or {}),
    }


def _twiml(message: str) -> str:
    # Simple TwiML response body
    safe = (message or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"<Response><Message>{safe}</Message></Response>"


def _parse_event(event):
    """Return (is_http, method, headers, query, body_raw, body_json, body_form)"""
    is_http = isinstance(event, dict) and (event.get("version") == "2.0" or event.get("requestContext", {}).get("http"))
    method = (event.get("requestContext", {}).get("http", {}).get("method") if is_http else None) or event.get("httpMethod")
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    query = event.get("queryStringParameters") or {}
    body_raw = event.get("body")
    if body_raw and event.get("isBase64Encoded"):
        import base64
        body_raw = base64.b64decode(body_raw).decode("utf-8")
    body_json = None
    body_form = {}
    ctype = headers.get("content-type", "")
    try:
        if body_raw and "application/json" in ctype:
            body_json = json.loads(body_raw)
        elif body_raw and ("application/x-www-form-urlencoded" in ctype or "multipart/form-data" in ctype):
            parsed = parse_qs(body_raw)
            body_form = {k: v[0] if isinstance(v, list) and v else v for k, v in parsed.items()}
        elif body_raw and not ctype:
            # Twilio sometimes sends without explicit header; try parse_qs then JSON
            parsed = parse_qs(body_raw)
            if parsed:
                body_form = {k: v[0] if isinstance(v, list) and v else v for k, v in parsed.items()}
            else:
                body_json = json.loads(body_raw)
    except Exception:
        pass
    return is_http, (method or "GET").upper(), headers, query, body_raw, body_json, body_form


def _upsert_subscriber(phone: str, status: str, source: str, evidence: dict):
    table = _get_table()
    item = {
        "phone": phone,
        "channel": "whatsapp",
        "consent_purpose": "daily_mitzvot",
        "consent_status": status,  # opted_in | opted_out
        "source": source,
        "evidence": evidence,
        "timestamp_iso": _now_iso(),
        "updated_by": "system",
    }
    table.put_item(Item=item)
    return item


def _get_subscriber(phone: str):
    """Fetch an existing subscriber record by phone, if present."""
    try:
        table = _get_table()
        resp = table.get_item(Key={"phone": phone})
        return resp.get("Item")
    except Exception:
        return None


def _handle_twilio_inbound(headers, form):
    body_text = (form.get("Body") or "").strip()
    from_num = _strip_channel_prefix(form.get("From") or "")
    to_num = _strip_channel_prefix(form.get("To") or "")
    message_sid = form.get("MessageSid") or form.get("SmsMessageSid") or ""

    txt = body_text.lower()
    # Fetch current status (for idempotent confirmations)
    existing = _get_subscriber(from_num) or {}
    current_status = existing.get("consent_status")

    # STATUS inquiry (respond with current state and guidance)
    if txt.startswith("status"):
        if not existing:
            return _respond(200, _twiml("You are not subscribed yet. Reply JOIN MITZVAH to subscribe, or STOP to opt out."), is_xml=True)
        if current_status == "opted_in":
            return _respond(200, _twiml("You’re subscribed to Daily Mitzvah. Reply STOP to opt out."), is_xml=True)
        if current_status == "opted_out":
            return _respond(200, _twiml("You are unsubscribed. Reply JOIN MITZVAH to re-subscribe."), is_xml=True)
        # Unknown/legacy state
        return _respond(200, _twiml("Your status is not set. Reply JOIN MITZVAH to subscribe, or STOP to opt out."), is_xml=True)
    # Treat exact STOP/UNSUBSCRIBE/CANCEL as opt-out
    if txt in ("stop", "unsubscribe", "cancel"):
        if current_status == "opted_out":
            return _respond(200, _twiml("You are already unsubscribed. Reply JOIN MITZVAH to re-subscribe."), is_xml=True)
        _upsert_subscriber(
            phone=from_num,
            status="opted_out",
            source="whatsapp_keyword",
            evidence={"messageSid": message_sid, "to": to_num},
        )
        return _respond(200, _twiml("You are unsubscribed. Reply JOIN MITZVAH to re-subscribe."), is_xml=True)

    # Allow opt-in via JOIN/START/YES/JOIN MITZVAH or the word SUBSCRIBE (but not 'unsubscribe')
    def _has_word(text: str, word: str) -> bool:
        t = " " + text.replace("\n", " ") + " "
        w = f" {word} "
        return w in t or t.startswith(w) or t.endswith(w)

    if (
        "join" in txt
        or "start" in txt
        or txt == "yes"
        or txt == "join mitzvah"
        or _has_word(txt, "subscribe")
    ):
        if current_status == "opted_in":
            return _respond(200, _twiml("You’re already subscribed to Daily Mitzvah. Reply STOP to opt out."), is_xml=True)
        _upsert_subscriber(
            phone=from_num,
            status="opted_in",
            source="whatsapp_keyword",
            evidence={"messageSid": message_sid, "to": to_num, "body": body_text},
        )
        return _respond(200, _twiml("You’re subscribed to Daily Mitzvah. Reply STOP to opt out."), is_xml=True)

    # Guidance fallback
    return _respond(200, _twiml("Reply JOIN MITZVAH to subscribe, or STOP to opt out."), is_xml=True)


def _handle_web_optin(query, body_json, body_form):
    phone = _strip_channel_prefix((body_form.get("phone") if body_form else None) or (body_json or {}).get("phone") or query.get("phone") or "")
    consent = (body_form.get("consent") if body_form else None) or (body_json or {}).get("consent") or query.get("consent") or ""
    action = (body_form.get("action") if body_form else None) or (body_json or {}).get("action") or query.get("action") or "optin"

    if not phone:
        return _respond(400, {"error": "Missing phone"})

    if action.lower() in ("optout", "unsubscribe", "stop"):
        _upsert_subscriber(phone=phone, status="opted_out", source="web_form", evidence={"action": action})
        return _respond(200, {"status": "ok", "message": "Unsubscribed"})

    # Treat consent truthy values as opt-in
    truthy = {"true", "1", "yes", "on", True}
    status = "opted_in" if (str(consent).lower() in truthy or action.lower() == "optin") else "opted_out"
    _upsert_subscriber(phone=phone, status=status, source="web_form", evidence={"action": action})
    return _respond(200, {"status": "ok", "message": "Subscribed" if status == "opted_in" else "Not subscribed"})


def lambda_handler(event, context):
    try:
        is_http, method, headers, query, body_raw, body_json, body_form = _parse_event(event)
        logger.info(f"Consent handler invoked: method={method} headers={list(headers.keys())}")

        if method == "GET":
            # Simple health/info endpoint
            return _respond(200, {
                "service": "consent",
                "time": _now_iso(),
                "table": os.environ.get("SUBSCRIBERS_TABLE", "unset"),
            })

        # POST: Twilio inbound vs web form
        if body_form.get("From") and (body_form.get("Body") or body_form.get("SmsBody")):
            return _handle_twilio_inbound(headers, body_form)

        return _handle_web_optin(query, body_json, body_form)

    except Exception as e:
        logger.exception("Consent handler error")
        return _respond(500, {"error": str(e)})
