"""
FINANCIAL RISK SCORING ENGINE
Formulas & Methodology:

1. Savings Rate (SR): (Total Income - Total Expenses) / Total Income
   - Goal: > 20% for maximum points.
2. Debt-to-Income (DTI): Total Debt / Total Income
   - Goal: < 36% (Industry standard).
3. Essential Spending Ratio (ESR): Total Essentials / Total Income
   - Goal: < 50% (50/30/20 rule).
4. Discretionary Spending Ratio (DSR): Total Non-Essentials / Total Income
   - Goal: < 30%.
5. Income Stability (IS): Coefficient of variation/Source count (Simulated)
   - Reward consistent income streams.
"""

def calculate_risk_score(transactions):
    """
    Fintech-grade risk assessment engine.
    Calculates a score (0-100) based on liquidity, debt, and spending efficiency.
    """
    # Group transactions
    income_txs = [tx for tx in transactions if tx.amount > 0]
    expense_txs = [tx for tx in transactions if tx.amount < 0]
    
    total_income = sum(tx.amount for tx in income_txs)
    total_expenses = abs(sum(tx.amount for tx in expense_txs))
    
    if total_income <= 0:
        return {
            "score": 0,
            "risk_level": "High",
            "metrics": {},
            "analysis": "Critical: No verified income detected. Financial insolvency risk is extremely high."
        }

    # 1. Savings Rate (Max 30 points)
    savings = total_income - total_expenses
    savings_rate = savings / total_income
    sr_score = max(0, min(30, (savings_rate / 0.20) * 30)) if savings_rate > 0 else 0

    # 2. Debt-to-Income (Max 20 points)
    # Categorized as 'Debt/Interest' in ai_service
    debt_payments = sum(abs(tx.amount) for tx in expense_txs if tx.category == "Debt/Interest")
    dti_ratio = debt_payments / total_income
    # Score decreases as DTI exceeds 36%
    dti_score = max(0, 20 - (max(0, dti_ratio - 0.10) / 0.26) * 20)

    # 3. Essential Spending (Max 25 points)
    # Goal: Essentials < 50% of income
    essential_cats = ["Rent/Mortgage", "Utilities", "Groceries", "Transport", "Health"]
    essentials = sum(abs(tx.amount) for tx in expense_txs if tx.category in essential_cats)
    esr_ratio = essentials / total_income
    esr_score = max(0, 25 - (max(0, esr_ratio - 0.30) / 0.50) * 25)

    # 4. Discretionary Ratio (Max 15 points)
    # Goal: < 30%
    discretionary_cats = ["Entertainment", "Dining Out", "Misc"]
    discretionary = sum(abs(tx.amount) for tx in expense_txs if tx.category in discretionary_cats)
    dsr_ratio = discretionary / total_income
    dsr_score = max(0, 15 - (max(0, dsr_ratio - 0.20) / 0.30) * 15)

    # 5. Income Stability (Max 10 points)
    # Simple proxy: number of deposits/consistency
    stability_score = min(10, len(income_txs) * 2.5)

    final_score = int(sr_score + dti_score + esr_score + dsr_score + stability_score)
    final_score = max(0, min(100, final_score))

    # Determine Risk Level
    if final_score >= 80:
        risk_level = "Low"
        analysis = "Strong financial health. High savings rate and controlled discretionary spending."
    elif final_score >= 50:
        risk_level = "Moderate"
        analysis = "Standard risk profile. Opportunities exist to optimize essential costs or increase savings."
    else:
        risk_level = "High"
        analysis = "Elevated risk detected. High debt-to-income or excessive discretionary spending relative to income."

    return {
        "score": final_score,
        "risk_level": risk_level,
        "analysis": analysis,
        "metrics": {
            "savings_rate": round(savings_rate, 2),
            "dti_ratio": round(dti_ratio, 2),
            "essential_ratio": round(esr_ratio, 2),
            "discretionary_ratio": round(dsr_ratio, 2)
        }
    }

def aggregate_report_data(transactions):
    """
    Aggregates transactions for frontend display and PDF.
    """
    categories = {}
    for tx in transactions:
        cat = tx.category or "Misc"
        categories[cat] = categories.get(cat, 0) + abs(tx.amount)
        
    return {
        "total_income": sum(tx.amount for tx in transactions if tx.amount > 0),
        "total_expenses": sum(abs(tx.amount) for tx in transactions if tx.amount < 0),
        "category_breakdown": categories
    }
