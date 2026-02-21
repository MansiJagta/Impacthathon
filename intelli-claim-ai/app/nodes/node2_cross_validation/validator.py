from datetime import datetime
from .fuzzy_match import similarity_score, is_match
from .duplicate_detector import detect_duplicates


# -----------------------------
# Helper extractors
# -----------------------------

def get_first(lst):
    return lst[0] if lst else None


def extract_all_fields(documents):

    names = []
    addresses = []
    policy_numbers = []
    bill_amounts = []
    dates = []

    for doc in documents:

        fields = doc.get("structured_fields", {})
        doc_type = doc.get("document_type")

        if doc_type == "policy":
            names.append(get_first(fields.get("holder_name", [])))
            addresses.append(get_first(fields.get("address", [])))
            policy_numbers.append(get_first(fields.get("policy_number", [])))

        elif doc_type == "bill":
            bill_amounts.append(get_first(fields.get("amount", [])))
            dates.append(get_first(fields.get("date", [])))
            names.append(get_first(fields.get("name", [])))

        elif doc_type == "id_proof":
            names.append(get_first(fields.get("name", [])))

        elif doc_type == "report":
            dates.append(get_first(fields.get("incident_date", [])))

    return {
        "names": [n for n in names if n],
        "addresses": [a for a in addresses if a],
        "policy_numbers": [p for p in policy_numbers if p],
        "bill_amounts": [a for a in bill_amounts if a],
        "dates": [d for d in dates if d],
    }


# -----------------------------
# VALIDATION FUNCTIONS
# -----------------------------

def validate_names(names):
    if len(names) < 2:
        return 1.0, []

    mismatches = []
    scores = []

    for i in range(len(names)-1):
        s = similarity_score(names[i], names[i+1])
        scores.append(s)
        if s < 0.85:
            mismatches.append(f"name mismatch: {names[i]} vs {names[i+1]}")

    return sum(scores)/len(scores), mismatches


def validate_policy_numbers(policy_numbers):
    if len(set(policy_numbers)) <= 1:
        return 1.0, []
    return 0.0, ["policy number mismatch across documents"]


def validate_amounts(amounts):
    if len(amounts) < 2:
        return 1.0, []

    amounts = [float(a) for a in amounts]
    max_amt = max(amounts)
    min_amt = min(amounts)

    if max_amt == 0:
        return 1.0, []

    diff_ratio = (max_amt - min_amt) / max_amt

    if diff_ratio > 0.2:
        return 0.5, [f"large amount discrepancy detected: {amounts}"]

    return 1.0, []


def validate_dates(dates):
    if len(dates) < 2:
        return 1.0, []

    parsed = []
    for d in dates:
        try:
            parsed.append(datetime.strptime(d, "%d/%m/%Y"))
        except:
            pass

    parsed.sort()

    if parsed != sorted(parsed):
        return 0.5, ["date chronology inconsistency"]

    return 1.0, []


# -----------------------------
# CONSISTENCY SCORE
# -----------------------------

def compute_consistency_score(scores):
    if not scores:
        return 1.0
    return sum(scores)/len(scores)


# -----------------------------
# MAIN NODE FUNCTION
# -----------------------------

def cross_validate(node1_output):

    documents = node1_output["documents"]

    # duplicate detection
    duplicate_docs = detect_duplicates(documents)

    extracted = extract_all_fields(documents)

    scores = []
    mismatches = []

    # name check
    s, m = validate_names(extracted["names"])
    scores.append(s)
    mismatches.extend(m)

    # policy number check
    s, m = validate_policy_numbers(extracted["policy_numbers"])
    scores.append(s)
    mismatches.extend(m)

    # amount check
    s, m = validate_amounts(extracted["bill_amounts"])
    scores.append(s)
    mismatches.extend(m)

    # date check
    s, m = validate_dates(extracted["dates"])
    scores.append(s)
    mismatches.extend(m)

    # duplicate check
    if duplicate_docs:
        mismatches.append(f"duplicate documents detected: {duplicate_docs}")
        scores.append(0.0)

    consistency_score = compute_consistency_score(scores)

    status = "PASS" if consistency_score >= 0.8 else "FAIL"

    return {
        "consistency_score": round(consistency_score, 2),
        "status": status,
        "mismatches": mismatches,
        "duplicate_documents": duplicate_docs
    }