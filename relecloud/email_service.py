"""Email service for ReleCloud application."""
from django.core.mail import send_mail
from django.conf import settings


def send_info_request_email(to_email: str, name: str, cruise: str) -> None:
    """
    Send an information request confirmation email to the user.

    Args:
        to_email: Recipient email address
        name: Requester's name
        cruise: Cruise name/title
    """
    subject = "ReleCloud: Information Request Confirmation"
    message = f"""
Hi {name},

Thank you for requesting information about {cruise}.

We will get back to you as soon as we have more details.

Best regards,
The ReleCloud Team
    """.strip()

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@relecloud.com')
    send_mail(subject, message, from_email, [to_email])
