# rules.py
class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field

def latest_financial_index(data: dict):
    for index, financial in enumerate(data.get("financials", [])):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index: int):
    financial = data["financials"][financial_index]
    return financial["pnl"]["lineItems"]["net_revenue"]

def total_borrowing(data: dict, financial_index: int):
    financial = data["financials"][financial_index]
    long_term_borrowings = financial["bs"]["liabilities"]["long_term_borrowings"]
    short_term_borrowings = financial["bs"]["liabilities"]["short_term_borrowings"]
    total_revenue_value = total_revenue(data, financial_index)
    return (long_term_borrowings + short_term_borrowings) / total_revenue_value if total_revenue_value > 0 else FLAGS.WHITE

def iscr(data: dict, financial_index: int):
    financial = data["financials"][financial_index]
    profit_before_tax = financial["pnl"]["lineItems"]["profit_before_tax"]
    depreciation = financial["pnl"]["lineItems"]["depreciation"]
    interest = financial["pnl"]["lineItems"]["interest"]

    iscr_value = (profit_before_tax + depreciation + 1) / (interest + 1)
    return iscr_value

def iscr_flag(data: dict, financial_index: int):
    iscr_value = iscr(data, financial_index)
    return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index: int):
    revenue = total_revenue(data, financial_index)
    return FLAGS.GREEN if revenue >= 50000000 else FLAGS.RED

def borrowing_to_revenue_flag(data: dict, financial_index: int):
    borrowing_ratio = total_borrowing(data, financial_index)
    return FLAGS.GREEN if borrowing_ratio <= 0.25 else FLAGS.AMBER
