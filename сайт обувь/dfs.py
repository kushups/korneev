import sqlite3

def create_connection(db_file):
    """Создает подключение к базе данных SQLite."""
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    """Создает таблицу users, если она не существует."""
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS users')  # Удаляем таблицу, если она существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            price REAL NOT NULL,
            tariff TEXT NOT NULL
        )
    ''')
    conn.commit()

def add_user(conn, username, email, price, tariff):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, email, price, tariff) VALUES (?, ?, ?, ?)
    ''', (username, email, price, tariff))
    conn.commit()
    print(f'Пользователь "{username}" добавлен в базу данных.')

def get_users(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ORDER BY id')
    return cursor.fetchall()

def clear_database(conn):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users')
    conn.commit()
    print('База данных очищена.')

def delete_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    if cursor.rowcount == 0:
        print(f'Пользователь с ID {user_id} не найден.')
    else:
        conn.commit()
        print(f'Пользователь с ID {user_id} удален из базы данных.')

def input_user_data(conn):
    username = input("Введите имя пользователя: ").strip()
    email = input("Введите email пользователя: ").strip()
    
    while True:
        try:
            price = float(input("Введите прайс пользователя: ").strip())
            break
        except ValueError:
            print("Ошибка: введите числовое значение для прайса.")
    
    tariff = input("Введите тариф пользователя: ").strip()
    add_user(conn, username, email, price, tariff)

def display_users(conn):
    users = get_users(conn)
    if not users:
        print("\nСписок пользователей пуст.")
    else:
        print("\nСписок всех пользователей:")
        print(f"{'ID':<4} {'Username':<20} {'Email':<30} {'Price':<10} {'Tariff'}")
        print("-" * 75)
        for user in users:
            print(f"{user[0]:<4} {user[1]:<20} {user[2]:<30} {user[3]:<10.2f} {user[4]}")

def main():
    conn = create_connection('user_database.db')
    create_table(conn)
    try:
        while True:
            display_users(conn)
            action = input(
                "\nВыберите действие: добавить / очистить / удалить / выход: "
            ).strip().lower()

            if action == 'добавить':
                input_user_data(conn)
            elif action == 'очистить':
                confirm = input("Вы уверены, что хотите очистить базу? (да/нет): ").strip().lower()
                if confirm == 'да':
                    clear_database(conn)
            elif action == 'удалить':
                try:
                    user_id = int(input("Введите ID пользователя для удаления: ").strip())
                    delete_user_by_id(conn, user_id)
                except ValueError:
                    print("Ошибка: ID должен быть целым числом.")
            elif action == 'выход':
                print("Выход из программы.")
                break
            else:
                print("Неверная команда. Пожалуйста, попробуйте снова.")
    finally:
        conn.close()

if __name__ == '__main__':
    main()
