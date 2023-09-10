import sqlite3 as sq


def get_con():
    with sq.connect('test.db') as con:
        print('Connection complete...')

        cur = con.cursor()

        def get_buy():
            emitent = input('Enter emitent: ')
            ticker = input('Enter ticket: ')
            date = input('Enter date: ')
            price = int(input('Enter price: '))
            quantity = int(input('Enter quantity: '))

            cur.execute(f'CREATE TABLE IF NOT EXISTS {emitent} (id INTEGER PRIMARY KEY, ticker TEXT, date TEXT, price INTEGER, quantity INTEGER)')
            cur.execute(f'INSERT INTO {emitent} (ticker, date, price, quantity) VALUES (?, ?, ?, ?)', (ticker, date, price, quantity))


        def get_sell():
            pass

        def get_show():
            pass

        choice = int(input('Buy: 1\nSell: 2\nShow portfolio: 3\nEnter your chois: '))

        if choice == 1:
            get_buy()
        elif choice == 2:
            get_sell()
        elif choice == 3:
            get_show()
        else:
            print('Wrong enter')

        cur = con.cursor()
        # cur.execute(
        #     'CREATE TABLE IF NOT EXISTS emmitent (id INTEGER PRIMARY KEY, name TEXT, ticker TEXT, amount INTEGER)')

        # name = input('Введите название эммитента: ')
        # ticker = input('Введите тикер эммитента: ')
        # amount = int(input('Введите количество акций: '))
        # cur.execute('INSERT INTO emmitent (name, ticker, amount) VALUES (?,?,?)', (name, ticker, amount))

        # cur.execute('''PRAGMA table_info(emmitent)''')
        # print(cur.fetchall())


if __name__ == '__main__':
    get_con()
