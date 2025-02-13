from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_user(telegram_id):
    """Получает имя пользователя и баланс"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, balance FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"username": user[0], "balance": user[1]}
    return {"error": "User not found"}

@app.route("/user/<int:telegram_id>")
def user_info(telegram_id):
    return jsonify(get_user(telegram_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
