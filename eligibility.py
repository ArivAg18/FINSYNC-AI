def analyze_eligibility(income, expenses, emi):
    emi_ratio = emi / income if income > 0 else 1
    stress_score = max(0, 100 - (emi_ratio * 100))

    if expenses >= income:
        return {
            "eligibility_score": 0,
            "reason": "Expenses exceed income.",
            "emi_ratio": round(emi_ratio, 2),
            "stress_score": round(stress_score, 2)
        }

    if emi_ratio > 0.5:
        score = 20
        reason = "Very high EMI burden."
    elif emi_ratio > 0.4:
        score = 40
        reason = "High EMI burden."
    elif emi_ratio > 0.3:
        score = 60
        reason = "Moderate EMI burden."
    else:
        score = 85
        reason = "Low EMI burden."

    return {
        "eligibility_score": score,
        "reason": reason,
        "emi_ratio": round(emi_ratio, 2),
        "stress_score": round(stress_score, 2)
    }


def generate_suggestions(income, expenses, emi_ratio, stress_score):
    s = []

    if emi_ratio > 0.4:
        s.append("EMI too high — reduce loan amount or increase tenure.")

    if expenses > income * 0.5:
        s.append("Reduce monthly expenses to improve savings.")

    if stress_score < 50:
        s.append("Loan may create financial stress.")

    if stress_score >= 70:
        s.append("Your financial standing is stable.")

    if not s:
        s.append("Loan profile looks healthy.")

    return s
