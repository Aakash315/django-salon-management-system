import re
import secrets

def normalize_phone(phone):

    phone = re.sub(
        r"\D",
        "",
        phone or ""
    )

    if len(phone) == 10:
        phone = "91" + phone

    if len(phone) == 12 and phone.startswith("91"):
        return "+" + phone

    return None

def generate_otp():
    return str(secrets.randbelow(900000) + 100000)