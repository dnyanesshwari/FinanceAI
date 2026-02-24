# app/services/finance_tools.py

import math

def calculate_emi(principal: float, rate: float, time_years: float):
    monthly_rate = rate / 12 / 100
    months = time_years * 12

    emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / \
          ((1 + monthly_rate) ** months - 1)

    return round(emi, 2)


def calculate_simple_interest(principal: float, rate: float, time_years: float):
    interest = (principal * rate * time_years) / 100
    return round(interest, 2)


def calculate_compound_interest(principal: float, rate: float, time_years: float):
    amount = principal * (1 + rate / 100) ** time_years
    return round(amount - principal, 2)
