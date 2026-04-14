def calculate_emi_details(principal, annual_rate, tenure_months):
    monthly_rate = (annual_rate / 100) / 12

    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (
            ((1 + monthly_rate) ** tenure_months) - 1
        )

    total_payable = emi * tenure_months
    total_interest = total_payable - principal

    return {
        "emi": round(emi, 2),
        "total_payable": round(total_payable, 2),
        "total_interest": round(total_interest, 2)
    }
