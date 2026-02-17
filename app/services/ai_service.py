import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CATEGORIES = [
    "Groceries", "Rent/Mortgage", "Utilities", "Entertainment", 
    "Dining Out", "Transport", "Health", "Debt/Interest", 
    "Savings/Investment", "Income", "Misc"
]

def categorize_transactions(transactions_list):
    """
    transactions_list: list of dicts with 'description' and 'amount'
    Returns: list of categorized transactions
    """
    if not os.getenv("OPENAI_API_KEY"):
        # Fallback for development without API key
        return [{"category": "Misc", **tx} for tx in transactions_list]

    prompt = f"""
    Categorize the following bank transactions into one of these categories: {', '.join(CATEGORIES)}.
    Format the output as a JSON list of strings (categories only) in the same order as the input.
    Input: {[tx['description'] for tx in transactions_list]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        data = json.loads(response.choices[0].message.content)
        categories = data.get("categories", ["Misc"] * len(transactions_list))
        
        for i, tx in enumerate(transactions_list):
            tx['category'] = categories[i] if i < len(categories) else "Misc"
        
        return transactions_list
    except Exception as e:
        print(f"AI categorization error: {e}")
        # Fallback
        for tx in transactions_list:
            tx['category'] = "Misc"
        return transactions_list
