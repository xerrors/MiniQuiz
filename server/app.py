from flask import Flask, request, jsonify, session, make_response
from flask_cors import CORS
from time import sleep
import sqlite3
import random

app = Flask(__name__)
# 以下CORS配置已取消注释
CORS(app)  # 允许所有来源

# 添加 after_request 装饰器以手动处理 CORS
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# 处理 OPTIONS 请求
@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    return jsonify({}), 200

app.secret_key = 'super_secret_key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/get_random_questions', methods=['POST'])
def get_random_questions():
    data = request.json
    count = data.get('count', 20)  # 默认获取20个问题

    conn = get_db_connection()
    try:
        # 从数据库获取所有问题
        questions = conn.execute('SELECT * FROM questions').fetchall()
        conn.close()

        # 转换为列表，并随机排序
        questions_list = [dict(q) for q in questions]
        random.shuffle(questions_list)

        # 返回指定数量的问题
        selected_questions = questions_list[:count]

        return jsonify({"questions": selected_questions, "ok": True}), 200
    except Exception as e:
        conn.close()
        return jsonify({"message": f"获取题目失败: {str(e)}"}), 500

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    sid = data.get('sid')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE sid = ? AND password = ?', (sid, password)).fetchone()
    conn.close()
    sleep(0.5) # 为了防止暴力破解，延迟 0.1 秒（为了用户体验哈哈哈）

    if user:
        session['user_id'] = user['id']
        return jsonify({"name": user['name'], "sid": user["sid"], "role": user["role"], "ok": True}), 200  # 返回用户名
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@app.route('/save_records', methods=['POST'])
def save_records():
    data = request.json
    sid = data.get('sid')
    name = data.get('name')
    questions = data.get('questions')
    answers = data.get('answers')
    score = data.get('score')
    date = data.get('date')

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO records (sid, name, questions, answers, score, date) VALUES (?, ?, ?, ?, ?, ?)',
                    (sid, name, questions, answers, score, date))
        conn.commit()
        conn.close()
        return jsonify({"message": "Record saved successfully", "ok": True}), 200
    except sqlite3.OperationalError as e:
        if 'conn' in locals():
            conn.close()
        return jsonify({"message": f"Database error: {e}", "ok": False}), 500
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        return jsonify({"message": f"Error: {str(e)}", "ok": False}), 500

@app.route('/get_records', methods=['POST'])
def get_records():
    data = request.json
    sid = data.get('sid')

    conn = get_db_connection()
    records = conn.execute('SELECT * FROM records WHERE sid = ?', (sid,)).fetchall()
    conn.close()

    return jsonify({"data": [dict(record) for record in records], "ok": True}), 200


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200


@app.route('/admin_get_records', methods=['POST'])
def admin_get_records():

    data = request.json
    sid = data.get('sid')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE sid = ?', (sid,)).fetchone()
    conn.close()
    sleep(0.5) # 为了防止暴力破解，延迟 0.1 秒（为了用户体验哈哈哈）

    if not user or user['role'] != 'admin':
        return jsonify({"message": "Invalid credentials"}), 401

    conn = get_db_connection()
    records = conn.execute('SELECT * FROM records').fetchall()
    conn.close()

    return jsonify({"data": [dict(record) for record in records], "ok": True}), 200


@app.route('/get_all_users', methods=['POST'])
def get_all_users():
    data = request.json
    sid = data.get('sid')

    # 验证是否为管理员
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE sid = ?', (sid,)).fetchone()

    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({"message": "无权访问"}), 401

    # 获取所有普通用户，过滤掉管理员
    users = conn.execute('SELECT id, sid, name, role, class FROM users').fetchall()
    conn.close()

    return jsonify({"users": [dict(user) for user in users], "ok": True}), 200


if __name__ == '__main__':
    app.run(debug=True)
