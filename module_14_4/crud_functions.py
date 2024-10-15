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
