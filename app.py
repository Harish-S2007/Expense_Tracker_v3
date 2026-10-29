
import os
import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

DATA_DIR = os.environ.get("DATA_DIR", "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB = os.path.join(DATA_DIR, "expenses.db")


def connect_db():
    return sqlite3.connect(DB)


def initialize_db():
    with connect_db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)


initialize_db()

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Expense Tracker - Version 3</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h1>Expense Tracker - Version 3</h1>

    <h2>Add Expense</h2>

    {% if message %}
        <p>{{ message }}</p>
    {% endif %}

    <form method="POST" action="/add">
        <label>Amount (₹):</label>
        <input type="number" name="amount" min="0.01"
               step="0.01" required><br><br>

        <label>Category:</label>
        <select name="category" required>
            <option value="Food">Food</option>
            <option value="Travel">Travel</option>
            <option value="Shopping">Shopping</option>
            <option value="Education">Education</option>
            <option value="Other">Other</option>
        </select><br><br>

        <label>Description:</label>
        <input type="text" name="description" required><br><br>

        <label>Date:</label>
        <input type="date" name="date" required><br><br>

        <button type="submit">Add Expense</button>
    </form>

    <h2>Total Expenses: ₹{{ "%.2f"|format(total) }}</h2>

    <h2>View Expenses</h2>
    {% if expenses %}
    <table border="1" cellpadding="8">
        <tr>
            <th>ID</th>
            <th>Amount (₹)</th>
            <th>Category</th>
            <th>Description</th>
            <th>Date</th>
        </tr>
        {% for e in expenses %}
        <tr>
            <td>{{ e[0] }}</td>
            <td>{{ "%.2f"|format(e[1]) }}</td>
            <td>{{ e[2] }}</td>
            <td>{{ e[3] }}</td>
            <td>{{ e[4] }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
        <p>No expenses recorded yet.</p>
    {% endif %}
</body>
</html>
"""


@app.route("/")
def home():
    with connect_db() as con:
        expenses = con.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
            ORDER BY id DESC
        """).fetchall()

        total = con.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
        """).fetchone()[0]

    return render_template_string(
        PAGE, expenses=expenses, total=total, message=""
    )


@app.route("/add", methods=["POST"])
def add_expense():
    try:
        amount = float(request.form["amount"])
        category = request.form["category"]
        description = request.form["description"].strip()
        date = request.form["date"]

        if amount <= 0 or not description or not date:
            raise ValueError("Invalid expense")

        with connect_db() as con:
            con.execute("""
                INSERT INTO expenses
                (amount, category, description, date)
                VALUES (?, ?, ?, ?)
            """, (amount, category, description, date))

    except (ValueError, KeyError):
        return "Enter valid expense details.", 400

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
