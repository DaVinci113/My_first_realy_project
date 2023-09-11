import sqlite3 as sq


def get_con():
    with sq.connect('test.db') as con:
        print('Connection complete...')

        cur = con.cursor()

        def get_buy():

            def get_match(emitent):
                cur.execute('SELECT emitent FROM portfolio')
                res = cur.fetchall()
                return any(emitent in x for x in res)

            def get_pos_cost(emitent):  # Расчет pos_cost
                cur.execute(f'SELECT cost FROM {emitent}')
                cost = cur.fetchall()
                result = 0
                for _ in cost:
                    result += int(_[0])
                return result

            def get_pos_quantity(emitent):  # Расчет pos_quantity
                cur.execute(f'SELECT quantity FROM {emitent}')
                quantity = cur.fetchall()
                result = 0
                for _ in quantity:
                    result += int(_[0])
                return result

            def get_pos_price(emitent):
                return 1000

            def get_profit(emitent):
                return get_pos_cost(emitent) - get_pos_price(emitent)

            emitent = input('Enter emitent: ')
            ticker = input('Enter ticker: ')
            date = input('Enter date: ')
            price = int(input('Enter price: '))
            quantity = int(input('Enter quantity: '))
            cost = price * quantity

            cur.execute(
                f'CREATE TABLE IF NOT EXISTS {emitent} (id INTEGER PRIMARY KEY, date TEXT, price INTEGER, quantity INTEGER, cost INTEGER)')
            cur.execute(f'INSERT INTO {emitent} (date, price, quantity, cost) VALUES (?, ?, ?, ?)',
                        (date, price, quantity, cost))

            cur.execute(
                'CREATE TABLE IF NOT EXISTS portfolio (id INTEGER PRIMARY KEY, emitent TEXT, ticker TEXT, pos_quantity INTEGER, pos_price INTEGER, pos_cost INTEGER, profit)')  # Создание таблицы portfolio

            if not get_match(emitent):
                cur.execute(
                    'INSERT INTO portfolio (emitent, ticker, pos_quantity, pos_price, pos_cost, profit) VALUES (?, ?, ?, ?, ?, ?)',
                    (emitent, ticker, quantity, price, get_pos_cost(emitent),
                     get_profit(emitent)))
            cur.execute(
                'UPDATE portfolio SET pos_quantity = ?, pos_price = ?, pos_cost = ?, profit = ? WHERE emitent = ?',
                (get_pos_quantity(emitent), get_pos_price(emitent), get_pos_cost(emitent),
                 get_profit(emitent), emitent))

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

        # cur.execute('''PRAGMA table_info(emmitent)''')
        # print(cur.fetchall())


if __name__ == '__main__':
    get_con()
