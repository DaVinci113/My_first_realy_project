import mysql.connector
from mysql.connector import Error
from config import host, port, user, password


def get_con():
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

    except Exception as ex:
        print(f'Not connection...{ex}')


if __name__ == '__main__':
    get_con()
