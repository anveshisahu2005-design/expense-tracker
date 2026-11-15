"""
Expense Tracker - ek simple Flask web app.

Kya karta hai:
- Income aur expense add karna (title, amount, category, date ke saath)
- Sab transactions ki list, total income, total expense aur balance dikhana
- Category-wise expense summary
- Transaction delete karna

Tech stack: Python (Flask) + SQLite + HTML/CSS (Jinja templates)
Run karne ke liye:  pip install -r requirements.txt  &&  python app.py
"""

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Database file project folder ke andar hi banegi (koi setup nahi chahiye)
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.db")

# Category list ek jagah rakhi hai taaki form me dropdown ban sake
CATEGORIES = ["Food", "Travel", "Rent", "Shopping", "Bills", "Education", "Salary", "Other"]


def get_db():
    """Naya database connection deta hai. Har request apna connection kholti hai."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # rows ko dictionary jaise use karne ke liye
    return conn


def init_db():
    """App start hote hi table bana deta hai (agar pehle se nahi hai)."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            title    TEXT NOT NULL,
            amount   REAL NOT NULL,
            type     TEXT NOT NULL CHECK (type IN ('income', 'expense')),
            category TEXT NOT NULL,
            date     TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    """Home page: saari transactions + income/expense/balance summary."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM transactions ORDER BY date DESC, id DESC"
    ).fetchall()
    conn.close()

    income = sum(r["amount"] for r in rows if r["type"] == "income")
    expense = sum(r["amount"] for r in rows if r["type"] == "expense")
    return render_template(
        "index.html",
        transactions=rows,
        income=income,
        expense=expense,
        balance=income - expense,
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    """GET: nayi entry ka form dikhata hai. POST: form ko database me save karta hai."""
    if request.method == "POST":
        title = request.form["title"].strip()
        amount = float(request.form["amount"])
        ttype = request.form["type"]            # 'income' ya 'expense'
        category = request.form["category"]
        date = request.form["date"] or datetime.now().strftime("%Y-%m-%d")

        conn = get_db()
        # ? placeholders use kiye hain - ye SQL injection se bachata hai
        conn.execute(
            "INSERT INTO transactions (title, amount, type, category, date) VALUES (?, ?, ?, ?, ?)",
            (title, amount, ttype, category, date),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template(
        "add.html", categories=CATEGORIES, today=datetime.now().strftime("%Y-%m-%d")
    )


@app.route("/delete/<int:txn_id>", methods=["POST"])
def delete(txn_id):
    """Ek transaction delete karta hai (sirf POST se, taaki galti se link click se na ho)."""
    conn = get_db()
    conn.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/summary")
def summary():
    """Category-wise kharch ka total dikhata hai."""
    conn = get_db()
    rows = conn.execute(
        "SELECT category, SUM(amount) AS total FROM transactions "
        "WHERE type = 'expense' GROUP BY category ORDER BY total DESC"
    ).fetchall()
    conn.close()
    return render_template("summary.html", rows=rows)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)  # debug=True sirf development ke liye, production me False
