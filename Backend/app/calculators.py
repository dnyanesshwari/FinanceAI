import math


def calculate_interest(principal: float, annual_rate: float, tenure_years: int, interest_type: str):
    """
    principal: loan amount
    annual_rate: annual interest rate in %
    tenure_years: number of years
    interest_type: 'simple' or 'compound'
    """

    rate = annual_rate / 100

    if interest_type.lower() == "simple":
        interest = principal * rate * tenure_years
        total_amount = principal + interest

        return {
            "type": "Simple Interest",
            "principal": principal,
            "interest": round(interest, 2),
            "total_amount": round(total_amount, 2)
        }

    elif interest_type.lower() == "compound":
        total_amount = principal * math.pow((1 + rate), tenure_years)
        interest = total_amount - principal

        return {
            "type": "Compound Interest",
            "principal": principal,
            "interest": round(interest, 2),
            "total_amount": round(total_amount, 2)
        }

    else:
        return {
            "error": "Invalid interest type. Use 'simple' or 'compound'."
        }
