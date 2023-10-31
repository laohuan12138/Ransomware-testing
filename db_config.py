import pymysql

def create_database_if_not_exists(connection, db_name):
    cursor = connection.cursor()
    cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
    result = cursor.fetchone()

    if not result:
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"[!] Database '{db_name}' created.")
    else:
        print(f"[!] Database '{db_name}' already exists.")

def create_table_if_not_exists(connection, db_name, table_name):
    cursor = connection.cursor()
    cursor.execute(f"USE {db_name}")
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()

    if not result:
        cursor.execute(f"CREATE TABLE {table_name}(id INT PRIMARY KEY AUTO_INCREMENT, computer_info VARCHAR(255),keyinfo VARBINARY(255))")
        print(f"[!] Table '{table_name}' created.")
    else:
        print(f"[!] Table '{table_name}' already exists.")

# 连接数据库
connection = pymysql.connect(
    host='127.0.0.1',  # 数据库地址
    user='root',  # 用户名
    password='123456',  # 密码
    autocommit=True
)


def db_reset():
    # 指定数据库和表名
    database_name = 'encrypt'
    table_name = 'KeyInfo'

    # 创建数据库（如果不存在）
    create_database_if_not_exists(connection, database_name)

    # 选择数据库
    connection.select_db(database_name)

    # 创建表（如果不存在）
    create_table_if_not_exists(connection, database_name, table_name)

    # 关闭连接
    connection.close()

if __name__ == "__main__":
    db_reset()