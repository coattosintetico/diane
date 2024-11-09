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
    Handles trailing whitespace and newlines to ensure consistent formatting.
    """
    expense_line = f"{expense.description.lower()},{expense.amount},{datetime.now().day},{expense.category.value}\n"

    # Raise error if the file doesn't exist
    if not EXPENSES_FILE.exists():
        print("\t⚠️ ERROR! the expenses .csv file doesn't exist")
        print(EXPENSES_FILE)
        print("skipping...")
        return

    # Read existing content and clean it
    content = EXPENSES_FILE.read_text().rstrip()

    # Write back with new expense, ensuring exactly one newline between entries
    with open(EXPENSES_FILE, "w") as file:
        file.write(content + "\n" + expense_line)

    return
