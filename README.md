# Expense Tracker

Ek simple, complete web app jo daily income aur expense track karta hai.
BCA final-year ke liye banaya gaya hai: code chhota hai, comments ke saath,
aur interview me aasaani se explain kiya ja sakta hai.

## Features
- Income / expense entry (title, amount, type, category, date)
- Home page par total income, total expense aur balance cards
- Transactions table, delete option ke saath
- Category-wise expense summary (bar chart)
- SQLite database - koi alag database server install karne ki zaroorat nahi

## Tech Stack
- **Python 3 + Flask** - backend (routes, forms, database logic)
- **SQLite** - database (`expenses.db` file apne aap ban jaati hai)
- **HTML + CSS (Jinja templates)** - frontend

## Kaise Run Karein
```bash
pip install -r requirements.txt
python app.py
```
Phir browser me kholo: http://127.0.0.1:5000

## Project Structure
```
expense-tracker/
├── app.py               # pura backend: routes + database code
├── requirements.txt     # Python dependencies
├── templates/           # HTML pages (Jinja templates)
│   ├── base.html        # common layout (navbar)
│   ├── index.html       # home: summary cards + transactions table
│   ├── add.html         # nayi entry ka form
│   └── summary.html     # category-wise bar chart
└── static/
    └── style.css        # styling
```

## Database Schema
Ek hi table hai - `transactions`:

| Column   | Type    | Matlab                                |
|----------|---------|---------------------------------------|
| id       | INTEGER | auto-increment primary key            |
| title    | TEXT    | entry ka naam (e.g. "Grocery")        |
| amount   | REAL    | kitne rupaye                          |
| type     | TEXT    | 'income' ya 'expense' (CHECK laga hai)|
| category | TEXT    | Food, Travel, Rent, ...               |
| date     | TEXT    | YYYY-MM-DD format                     |
