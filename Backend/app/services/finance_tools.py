# app/services/finance_tools.py

import math

def calculate_emi(principal: float, rate: float, time_years: float):
    if principal < 0 or rate < 0 or time_years <= 0:
        raise ValueError("Principal and rate must be non-negative, and time must be positive.")

    monthly_rate = rate / 12 / 100
    months = time_years * 12

    if monthly_rate == 0:
        return round(principal / months, 2)

    emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / \
          ((1 + monthly_rate) ** months - 1)

    return round(emi, 2)


def calculate_simple_interest(principal: float, rate: float, time_years: float):
    if principal < 0 or rate < 0 or time_years < 0:
        raise ValueError("Principal, rate, and time must be non-negative.")
    interest = (principal * rate * time_years) / 100
    return round(interest, 2)


def calculate_compound_interest(principal: float, rate: float, time_years: float):
    if principal < 0 or rate < 0 or time_years < 0:
        raise ValueError("Principal, rate, and time must be non-negative.")
    amount = principal * (1 + rate / 100) ** time_years
    return round(amount - principal, 2)
