import sqlite3


connection = sqlite3.connect('database.db')    # подключаемся к базе данных, указываем ее название
cursor = connection.cursor()


def initiate_db():    # функция создания таблицы, если ее еще не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL, 
    balance INT NOT NULL
    );
    ''')


initiate_db()


def add_products(title, description, price):    # Функция добавления товаров в БД
    check_products = cursor.execute('SELECT * FROM Products WHERE title = ?', (title,))  # проверяем наличие товара с таким же названием в базе данных

    if check_products.fetchone() is None:  # если значение check_products по введенному 'title' не найдено, то добавляем продукт в БД
        cursor.execute(f'''
        INSERT INTO Products (title, description, price) VALUES('{title}', '{description}', '{price}')
        ''')
    connection.commit()  # сохраняем состояние БД после добавления товаров


for i in range(1, 5):    # с помощью цикла заполним базу данных однотипными данными
    add_products(f'Product {i}', f' Описание {i}', f'{i * 100}')


def get_all_products():    # возвращает все записи из таблицы Products
    cursor.execute('SELECT * FROM Products')    # запросили список продуктов
    products_list = cursor.fetchall()
    connection.commit()  # сохраняем изменения
    return products_list


def add_user(username, email, age):    # добавляет пользователей в таблицу Users
    cursor.execute(f'''
    INSERT INTO Users (username, email, age, balance) VALUES('{username}', '{email}', '{age}', 1000)
    ''')    # последнее значение '1000' означает, что 'balance' у новых пользователей = 1000
    connection.commit()  # сохраняем состояние БД


def is_included(username):    # принимает имя пользователя и возвращает True, если пользователь есть в таблице Users
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    connection.commit()
    if check_user is None:
        return False
    else:
        return True


connection.commit()    # сохраняем состояние
connection.close()    # закрываем подключение
