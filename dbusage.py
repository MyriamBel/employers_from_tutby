import sqlite3
#base name is db.sqlite

def availability_check(table_name):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    sql = "SELECT count (*) FROM '%s'" #Посчитаем количество столбцов в таблице
    try:
        cursor.execute(sql % table_name)
    except sqlite3.OperationalError: #Таблицы нет
        cursor.close()
        return 1
    else:
        cursor.close()
        return 0 #Все ок

def create_table(table_name):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    if table_name == 'company':
        sql_str = "CREATE TABLE company (idd integer NOT NULL PRIMARY KEY AUTOINCREMENT, url text NOT NULL, name text NOT NULL, description text)"
    cursor.execute(sql_str)
    conn.commit()
    cursor.close()

def add_to_db(anydict, table_name):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    if table_name == 'company':
        sql_str = "INSERT INTO company (url, name, description) VALUES (?, ?, ?)"
        cursor.execute(sql_str, [str(anydict['url']), str(anydict['name']), str(anydict['description'])])
    conn.commit()
    cursor.close()
