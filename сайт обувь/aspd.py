from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Функция для создания подключения к базе данных
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

# Функция для создания таблиц в базе данных
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            price REAL NOT NULL,
            tariff TEXT NOT NULL
        )
    ''')
    conn.commit()

# Функция для получения всех пользователей
def get_users(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ORDER BY id')
    return cursor.fetchall()

# Функция для получения пользователя по ID
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    return cursor.fetchone()

# Функция для получения следующего доступного ID
def get_next_id(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM users')
    max_id = cursor.fetchone()[0]
    return (max_id + 1) if max_id is not None else 1

# Главный маршрут приложения
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = create_connection('users.db')
    create_table(conn)

    if request.method == 'POST':
        if 'add' in request.form:
            username = request.form['username']
            email = request.form['email']
            price = request.form['price']
            tariff = request.form['tariff']
            next_id = get_next_id(conn)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (id, username, email, price, tariff) VALUES (?, ?, ?, ?, ?)', 
                           (next_id, username, email, price, tariff))
            conn.commit()
        elif 'delete' in request.form:
            user_id = request.form['user_id']
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
        elif 'clear' in request.form:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users')
            conn.commit()

    return render_template('index.html', users=get_users(conn))

# Маршрут для получения информации о пользователе по ID
@app.route('/user/<int:user_id>', methods=['GET'])
def user(user_id):
    conn = create_connection('users.db')
    user_data = get_user_by_id(conn, user_id)
    if user_data:
        return render_template('user.html', user=user_data)
    else:
        return "Пользователь не найден", 404

# Маршрут для поиска пользователя по ID
@app.route('/search', methods=['POST'])
def search():
    user_id = request.form['user_id']
    conn = create_connection('users.db')
    user_data = get_user_by_id(conn, user_id)
    if user_data:
        return render_template('user.html', user=user_data)
    else:
        return "Пользователь не найден", 404

if __name__ == '__main__':
    app.run(debug=True)
