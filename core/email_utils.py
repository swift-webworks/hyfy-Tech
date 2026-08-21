"""
Thin wrapper around the Resend API (https://resend.com) for sending
enquiry-notification and auto-reply emails.

Falls back gracefully (logs only) when RESEND_API_KEY is not configured,
so local development never breaks because email isn't set up.
"""

import logging

import requests
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

RESEND_ENDPOINT = "https://api.resend.com/emails"


def _send_via_resend(*, to, subject, html):
    if not settings.RESEND_API_KEY:
        logger.info("RESEND_API_KEY not set; skipping email send. Subject: %s", subject)
        return False

    try:
        response = requests.post(
            RESEND_ENDPOINT,
            headers={
                "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": settings.ENQUIRY_FROM_EMAIL,
                "to": [to] if isinstance(to, str) else to,
                "subject": subject,
                "html": html,
            },
            timeout=10,
        )
        response.raise_for_status()
        return True
    except requests.RequestException:
        logger.exception("Failed to send email via Resend (subject: %s)", subject)
        return False


def send_enquiry_notification(enquiry):
    """Notify the HY-FY team of a new enquiry."""
    html = render_to_string("emails/enquiry_notification.html", {"enquiry": enquiry})
    return _send_via_resend(
        to=settings.ENQUIRY_TO_EMAIL,
        subject=f"New Enquiry: {enquiry.coordinator_name} - {enquiry.get_service_required_display()}",
        html=html,
    )


def send_enquiry_autoreply(enquiry):
    """Optional confirmation email back to the person who submitted the form."""
    html = render_to_string("emails/enquiry_autoreply.html", {"enquiry": enquiry})
    return _send_via_resend(
        to=enquiry.email,
        subject="We've received your enquiry - HY-FY Technology",
        html=html,
    )
