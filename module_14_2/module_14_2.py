import sqlite3


connection = sqlite3.connect('not_telegram.db')    # подключаемся к базе данных, указываем ее название
cursor = connection.cursor()    # создали объект курсора

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')


""" Блок кода из предыдущей задачи 'module_14_1'.

# Заполнили таблицу Users, после чего закомментировали этот блок кода.
# for i in range(1, 11):
#     cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
#                    (f'User{i}', f'example{i}@gmail.com', f'{10 * i}', '1000'))


# Изменили 'balance' у каждой 2-ой записи, начиная с 1-ой на 500. После изменения закомментировали этот блок кода.
# for i in range(1, 11, 2):
#     cursor.execute('UPDATE Users SET balance = ? WHERE username = ?', (500, f'User{i}'))


# Удалили каждую 3-ую запись в таблице начиная с 1-ой, потом закомментировала этот блок кода.
# for i in range(1, 11, 3):
#     cursor.execute('DELETE FROM Users WHERE username = ?', (f'User{i}',))


# Сделали выборку всех записей, где возраст не равен 60 и вывели их в консоль.
cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
users = cursor.fetchall()
for user in users:
    print(f'Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')
"""


# Удалили из базы данных 'not_telegram.db' запись с id = 6.
cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

cursor.execute('SELECT COUNT(*) FROM Users')    # подсчитали общее количество записей
total_users = cursor.fetchone()[0]

cursor.execute('SELECT SUM(balance) FROM Users')    # посчитали сумму всех балансов
all_balances = cursor.fetchone()[0]
print(all_balances / total_users)    # вывели в консоль средний баланс всех пользователей


connection.commit()    # сохраняем состояние
connection.close()    # закрываем подключение
