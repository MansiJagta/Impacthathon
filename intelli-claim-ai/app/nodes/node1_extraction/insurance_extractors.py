import re


def extract_policy_number(text):
    patterns = [
        r"[A-Z]-\d+/\d+/\d+",
        r"[A-Z]{2,5}-\d{4,10}",
        r"[A-Z]{2,5}/\d{4,10}",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()

    return None


def extract_bill_amount(text):

    # Look for keyword-based detection
    patterns = [
        r"(Total|Amount|Payable|Grand Total)[^\d]{0,10}(₹?\s?\d{3,9})",
        r"₹\s?\d{3,9}",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Return only the numeric part
            for group in match.groups():
                if group and re.search(r"\d", group):
                    return group.strip()

    return None


def extract_vehicle_number(text):
    match = re.search(r"[A-Z]{2}\d{2}[A-Z]{2}\d{4}", text)
    return match.group() if match else None


def extract_property_address(text):
    match = re.search(r"\d{1,4}\s[A-Za-z\s]+", text)
    return match.group() if match else None