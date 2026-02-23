from datetime import datetime

def round_amount_check(amount):
    if amount % 1000 == 0:
        return True
    return False


def timing_check(policy_start, incident_date):
    days = (incident_date - policy_start).days
    if days < 7:
        return True
    return False