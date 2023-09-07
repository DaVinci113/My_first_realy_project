import pymysql
from config import host, user, password, db_name


def get_con():
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            port=3306,
            password=password,
            database=db_name
        )
        print('Successfully connection...')
        print('#'*20)

        try:
            with connection.cursor() as curs:
                curs.execute('SHOW DATABASES;')
                print(curs.fetchall())
        finally:
            connection.close()

    except Exception as ex:
        print(f'Not connection...{ex}')


if __name__ == '__main__':
    get_con()
