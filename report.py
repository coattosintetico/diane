import subprocess
from datetime import datetime
from pathlib import Path

import pandas as pd

EXPENSES_FILE = Path(
    f"/data/data/com.termux/files/home/storage/shared/Documents/obsidianRemoteVault/personal/expenses/{datetime.now().strftime('%Y-%m')}.csv.md"
)


def report():
    """
    Generates a small report of the expenses of the current month.

    Sum of amount expensed per category for current month.
    """
    print()
    print("╔═════════════════════════════╗")
    print("║ \033[3mM O N T H L Y   R E P O R T\033[0m ║")
    print("╚═════════════════════════════╝")
    print()

    df = pd.read_csv(EXPENSES_FILE)

    # Group by category and sum the amounts
    category_sums = df.groupby("category")["amount"].sum().reset_index()
    # exclude "hacendado"
    category_sums = category_sums[category_sums["category"] != "hacendado"]
    # compute total amount
    total = category_sums["amount"].sum()

    # Create a temporary .dat file for termgraph
    temp_file = Path("temp_expenses.dat")

    # Write the data in the format required by termgraph
    with open(temp_file, "w") as f:
        for _, row in category_sums.iterrows():
            f.write(f"{row['category']},{row['amount']}\n")

    try:
        # Execute termgraph command

        subprocess.run(["termgraph", "--width", "25", str(temp_file)], check=True)

        print()
        print("┌───")
        print(f"│ Total for this month: {total:.2f} €")
        print("└───")
    finally:
        print("cleaning up...")
        # Clean up the temporary file
        temp_file.unlink()


if __name__ == "__main__":
    report()
