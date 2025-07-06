import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
from collections import defaultdict

DATA_FILE = "expenses.json"

# ----------------- Data Handling Functions -----------------

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense(expenses, amount, category, date):
    expenses.append({
        "amount": float(amount),
        "category": category,
        "date": date
    })
    save_expenses(expenses)

def delete_expense(expenses, idx):
    if 0 <= idx < len(expenses):
        del expenses[idx]
        save_expenses(expenses)

def edit_expense(expenses, idx, amount, category, date):
    if 0 <= idx < len(expenses):
        expenses[idx] = {
            "amount": float(amount),
            "category": category,
            "date": date
        }
        save_expenses(expenses)

# ----------------- Summary Functions -----------------

def get_total_by_category(expenses, category):
    return sum(e["amount"] for e in expenses if e["category"] == category)

def get_total_spending(expenses):
    return sum(e["amount"] for e in expenses)

def get_spending_over_time(expenses, period="monthly"):
    summary = defaultdict(float)
    for e in expenses:
        date = datetime.strptime(e["date"], "%Y-%m-%d")
        if period == "daily":
            key = date.strftime("%Y-%m-%d")
        elif period == "weekly":
            key = f"{date.year}-W{date.isocalendar()[1]}"
        else:  # monthly
            key = date.strftime("%Y-%m")
        summary[key] += e["amount"]
    return dict(summary)

def get_categories(expenses):
    return sorted(set(e["category"] for e in expenses))

# ----------------- GUI Functions -----------------

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.expenses = load_expenses()
        self.create_menu()

    def create_menu(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()

        ttk.Label(frame, text="Personal Expense Tracker", font=("Arial", 16)).pack(pady=10)

        ttk.Button(frame, text="Add Expense", width=30, command=self.add_expense_window).pack(pady=5)
        ttk.Button(frame, text="View Summaries", width=30, command=self.view_summary_window).pack(pady=5)
        ttk.Button(frame, text="View/Edit/Delete Expenses", width=30, command=self.view_expenses_window).pack(pady=5)
        ttk.Button(frame, text="Exit", width=30, command=self.root.quit).pack(pady=5)

    def add_expense_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Expense")
        win.geometry("300x250")
        frame = ttk.Frame(win, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Amount:").pack(anchor="w")
        amount_entry = ttk.Entry(frame)
        amount_entry.pack(fill="x")

        ttk.Label(frame, text="Category:").pack(anchor="w")
        category_entry = ttk.Entry(frame)
        category_entry.pack(fill="x")

        ttk.Label(frame, text="Date (YYYY-MM-DD, optional):").pack(anchor="w")
        date_entry = ttk.Entry(frame)
        date_entry.pack(fill="x")

        def submit():
            amount = amount_entry.get()
            category = category_entry.get()
            date = date_entry.get().strip()
            if not amount or not category:
                messagebox.showerror("Error", "Amount and Category are required.")
                return
            try:
                float(amount)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")
                return
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            else:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Date format should be YYYY-MM-DD.")
                    return
            add_expense(self.expenses, amount, category, date)
            messagebox.showinfo("Success", "Expense added!")
            win.destroy()

        ttk.Button(frame, text="Add", command=submit).pack(pady=10)

    def view_summary_window(self):
        win = tk.Toplevel(self.root)
        win.title("Expense Summaries")
        win.geometry("400x400")
        frame = ttk.Frame(win, padding=10)
        frame.pack(fill="both", expand=True)

        # Total overall spending
        total = get_total_spending(self.expenses)
        ttk.Label(frame, text=f"Total Spending: ${total:.2f}", font=("Arial", 12)).pack(pady=5)

        # Spending by category
        ttk.Label(frame, text="Spending by Category:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        categories = get_categories(self.expenses)
        for cat in categories:
            cat_total = get_total_by_category(self.expenses, cat)
            ttk.Label(frame, text=f"{cat}: ${cat_total:.2f}").pack(anchor="w")

        # Spending over time
        ttk.Label(frame, text="Spending Over Time (Monthly):", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        monthly = get_spending_over_time(self.expenses, "monthly")
        for month, amt in sorted(monthly.items()):
            ttk.Label(frame, text=f"{month}: ${amt:.2f}").pack(anchor="w")

    def view_expenses_window(self):
        win = tk.Toplevel(self.root)
        win.title("All Expenses")
        win.geometry("500x400")
        frame = ttk.Frame(win, padding=10)
        frame.pack(fill="both", expand=True)

        columns = ("#","Amount", "Category", "Date")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)

        for idx, e in enumerate(self.expenses):
            tree.insert("", "end", iid=idx, values=(idx+1, f"${e['amount']:.2f}", e["category"], e["date"]))

        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "No expense selected.")
                return
            idx = int(selected[0])
            if messagebox.askyesno("Confirm", "Delete selected expense?"):
                delete_expense(self.expenses, idx)
                tree.delete(selected[0])

        def edit_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "No expense selected.")
                return
            idx = int(selected[0])
            e = self.expenses[idx]
            amount = simpledialog.askstring("Edit Amount", "Amount:", initialvalue=str(e["amount"]), parent=win)
            if amount is None:
                return
            category = simpledialog.askstring("Edit Category", "Category:", initialvalue=e["category"], parent=win)
            if category is None:
                return
            date = simpledialog.askstring("Edit Date", "Date (YYYY-MM-DD):", initialvalue=e["date"], parent=win)
            if date is None:
                return
            try:
                float(amount)
                datetime.strptime(date, "%Y-%m-%d")
            except Exception:
                messagebox.showerror("Error", "Invalid input.")
                return
            edit_expense(self.expenses, idx, amount, category, date)
            tree.item(selected[0], values=(idx+1, f"${float(amount):.2f}", category, date))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Delete Selected", command=delete_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit Selected", command=edit_selected).pack(side="left", padx=5)

# ----------------- Main -----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()