def calculate_credit_score(income, expenses, emi, stress_score):
    emi_ratio = emi / income if income > 0 else 1
    expense_ratio = expenses / income if income > 0 else 1

    score = 600

    if emi_ratio > 0.4:
        score -= 150
    else:
        score += 50

    if expense_ratio > 0.5:
        score -= 100
    else:
        score += 50

    if stress_score < 50:
        score -= 100
    else:
        score += 50

    score = max(300, min(900, score))

    status = (
        "Excellent" if score >= 750 else
        "Good" if score >= 650 else
        "Average" if score >= 550 else
        "Poor"
    )

    return {
        "score": score,
        "status": status
    }
