import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # Таблица пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        username TEXT,
        balance REAL DEFAULT 0.0
    );
    """)
    # Таблица заданий
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        reward REAL
    );
    """)
    conn.commit()
    conn.close()

# Получение данных пользователя по telegram_id
def get_user(telegram_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, balance FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return {"username": user[0], "balance": user[1]} if user else {"error": "User not found"}

# Обновление баланса пользователя
def update_balance(telegram_id, amount):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE telegram_id = ?", (amount, telegram_id))
    conn.commit()
    conn.close()

# Получение всех заданий
def get_tasks():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, reward FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return [{"id": task[0], "title": task[1], "description": task[2], "reward": task[3]} for task in tasks]

@app.route("/user/<int:telegram_id>")
def user_info(telegram_id):
    return jsonify(get_user(telegram_id))

@app.route("/tasks")
def tasks():
    return jsonify(get_tasks())

@app.route("/complete_task", methods=["POST"])
def complete_task():
    telegram_id = request.json.get("telegram_id")
    task_id = request.json.get("task_id")

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT reward FROM tasks WHERE id = ?", (task_id,))
    reward = cursor.fetchone()[0]

    # Обновляем баланс пользователя
    update_balance(telegram_id, reward)
    conn.close()

    return jsonify({"status": "success", "new_balance": get_user(telegram_id)["balance"]})

if __name__ == "__main__":
    init_db()  # Инициализация базы данных
    app.run(host="0.0.0.0", port=5000, debug=True)
