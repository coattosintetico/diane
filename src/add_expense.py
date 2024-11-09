from datetime import datetime
from pathlib import Path

from .llm_call import Expense

# get the current year and month in the format YYYY-MM
EXPENSES_FILE = Path(
    f"/data/data/com.termux/files/home/storage/shared/Documents/obsidianRemoteVault/personal/expenses/{datetime.now().strftime('%Y-%m')}.csv.md"
)


def add_expense(expense: Expense) -> None:
    """
    Adds an expense to the .csv file of the current month.
    """
    current_date = datetime.now().strftime("%d")

    with open(EXPENSES_FILE, "a") as file:
        file.write(f"{expense.description},{expense.amount},{current_date},{expense.category.value}\n")

    return
