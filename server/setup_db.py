import sqlite3
import pandas as pd
import os

def setup_database():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            sid TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT DEFAULT 'student',
            class TEXT NOT NULL
        )
    ''')

    # 创建答题记录表，包括学号、姓名、题目、答案、分数、时间
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY,
            sid TEXT NOT NULL,
            name TEXT NOT NULL,
            questions TEXT NOT NULL,
            answers TEXT NOT NULL,
            score INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # 创建题目表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            序号 INTEGER,
            题目 TEXT NOT NULL,
            A TEXT NOT NULL,
            B TEXT NOT NULL,
            C TEXT NOT NULL,
            D TEXT NOT NULL,
            答案 TEXT NOT NULL
        )
    ''')

    # 处理用户数据 - 使用 REPLACE 处理已存在的记录
    if os.path.exists('../data/users.csv'):
        print("正在导入用户数据...")
        # 读取CSV文件
        users_df = pd.read_csv('../data/users.csv')
        users = users_df.values.tolist()

        # 使用 INSERT OR REPLACE 语法来处理重复项
        for user in users:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO users (sid, password, name, role, class)
                    VALUES (?, ?, ?, ?, ?)
                ''', user)
                print(f"用户 {user[2]} ({user[0]}) 数据已导入/更新")
            except Exception as e:
                print(f"导入用户 {user[0]} 时出错: {e}")

        print(f"成功处理 {len(users)} 条用户记录")
    else:
        print("警告: 找不到用户数据文件 users.csv, 跳过")

    # 导入题库数据 - 也使用 REPLACE 处理已存在的记录
    # 先检查是否已有数据
    existing_questions = cursor.execute('SELECT COUNT(*) FROM questions').fetchone()[0]

    # 如果表为空或需强制更新题库数据
    csv_path = '../data/aigc.csv'

    if os.path.exists(csv_path):
        print(f"正在处理题库数据...")
        questions_df = pd.read_csv(csv_path)
        questions_data = questions_df.to_dict('records')

        # 统计新增和更新的题目数量
        new_count = 0
        update_count = 0

        for question in questions_data:
            # 检查题目是否已存在
            existing = cursor.execute(
                'SELECT id FROM questions WHERE 序号 = ?',
                (question['序号'],)
            ).fetchone()

            try:
                if existing:
                    # 更新现有题目
                    cursor.execute('''
                        UPDATE questions
                        SET 题目 = ?, A = ?, B = ?, C = ?, D = ?, 答案 = ?
                        WHERE 序号 = ?
                    ''', (
                        question['题目'],
                        question['A'],
                        question['B'],
                        question['C'],
                        question['D'],
                        question['答案'],
                        question['序号']
                    ))
                    update_count += 1
                else:
                    # 插入新题目
                    cursor.execute('''
                        INSERT INTO questions (序号, 题目, A, B, C, D, 答案)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        question['序号'],
                        question['题目'],
                        question['A'],
                        question['B'],
                        question['C'],
                        question['D'],
                        question['答案']
                    ))
                    new_count += 1
            except Exception as e:
                print(f"处理题目 #{question['序号']} 时出错: {e}")

        print(f"题库处理完成: 新增 {new_count} 题, 更新 {update_count} 题")
    else:
        print("警告: 找不到题库数据文件 aigc.csv")

    connection.commit()
    connection.close()
    print("数据库初始化完成")

if __name__ == '__main__':
    setup_database()
