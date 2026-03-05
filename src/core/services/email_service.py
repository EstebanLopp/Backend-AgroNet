from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_templated_email(
    *,
    subject: str,
    to: list[str],
    template_html: str,
    context: dict,
    template_txt: str | None = None,
    reply_to: list[str] | None = None,
) -> None:
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    html_body = render_to_string(template_html, context)
    text_body = render_to_string(template_txt, context) if template_txt else ""

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=to,
        reply_to=reply_to or None,
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)