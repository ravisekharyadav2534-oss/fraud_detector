"""Rule-based red-flag features shared by training and the app."""
import re

FREE_EMAIL = r"@(gmail|yahoo|outlook|hotmail|rediffmail|protonmail)\.(com|in)"
MONEY_ASK = r"(registration|training|security|processing|kit|application|refundable)\s*(fee|deposit|charge)|pay\s+(rs|inr|\$|usd)|send\s+(money|payment)"
CHAT_APPS = r"whatsapp|telegram|signal"
URGENCY = r"urgent|limited (seats|vacanc)|apply immediately|hurry|last date today"
NO_PROCESS = r"no interview|without interview|direct (joining|selection)|no experience (needed|required)|no skills"
TOO_GOOD = r"earn\s*(up to\s*)?(rs\.?|inr|\$)?\s*\d[\d,]*\s*(per|/)\s*(day|week)|work from home.*(guaranteed|100%)|guaranteed (income|job|salary)"

RULES = {
    "Asks for money / fee": MONEY_ASK,
    "Uses a free email domain (Gmail/Yahoo...)": FREE_EMAIL,
    "Pushes you to WhatsApp/Telegram": CHAT_APPS,
    "Urgency / pressure language": URGENCY,
    "No interview / no experience needed": NO_PROCESS,
    "Unrealistic or guaranteed income": TOO_GOOD,
}

def red_flags(text: str) -> list[str]:
    t = (text or "").lower()
    return [name for name, pat in RULES.items() if re.search(pat, t)]

def rule_features(texts):
    import pandas as pd
    rows = []
    for t in texts:
        t = (t or "").lower()
        rows.append({name: int(bool(re.search(p, t))) for name, p in RULES.items()})
    df = pd.DataFrame(rows)
    df["n_flags"] = df.sum(axis=1)
    df["length"] = [len(x or "") / 1000 for x in texts]
    return df.values

def extract_rules(df):
    """Picklable transformer function (no lambdas, so joblib can save it)."""
    return rule_features(list(df["text"]))
