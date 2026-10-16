from django.conf import settings


def company_info(request):
    """
    Makes company contact details available in every template
    (used in base.html header/footer, WhatsApp button, etc.)
    without having to pass them from every view.
    """
    return {
        "COMPANY_NAME": settings.COMPANY_NAME,
        "COMPANY_PHONE": settings.COMPANY_PHONE,
        "COMPANY_WHATSAPP": settings.COMPANY_WHATSAPP,
        "COMPANY_EMAIL": settings.COMPANY_EMAIL,
        "COMPANY_ADDRESS": settings.COMPANY_ADDRESS,
    }
