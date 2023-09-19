import sqlite3 as sq


def get_con():
    with sq.connect('test.db') as con:
        print('#' * 35, '\nConnection complete...\n#' + '#' * 34)

        cur = con.cursor()

        def get_pos_quantity(emitent):  # Расчет pos_quantity
            cur.execute(f'SELECT quantity FROM {emitent}')
            quantity = cur.fetchall()
            result = 0
            for _ in quantity:
                result += int(_[0])
            return result

        def get_buy():

            def get_current_price(emitent):
                return 1000

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

            def get_pos_price(emitent):
                return get_pos_quantity(emitent) * get_current_price(emitent)

            def get_profit(emitent):
                return get_pos_price(emitent) - get_pos_cost(emitent)

            cur.execute(
                'CREATE TABLE IF NOT EXISTS portfolio (emitent TEXT, ticker TEXT, pos_quantity INTEGER, pos_price INTEGER, pos_cost INTEGER, profit)')  # Создание таблицы portfolio

            get_show()

            answer = input('Add shares to existing?\nYes:Y\nNo:N\nAnswer: ')

            if answer.upper() == 'N':
                emitent = input('Enter emitent: ')
                ticker = input('Enter ticker: ')
            elif answer.upper() == 'Y':
                cur.execute('SELECT emitent FROM portfolio')
                print('#' * 35, '\nList of emitents from yours portfolio:')
                for i, j in enumerate(cur.fetchall()):
                    print(f'{j[0]}: {i + 1}')
                name = int(input('Select emitent to add: '))
                cur.execute(f'SELECT emitent FROM portfolio WHERE rowid = {name}')
                emitent = cur.fetchall()[0][0]

            date = input('Enter date: ')
            price = int(input('Enter price: '))
            quantity = int(input('Enter quantity: '))
            cost = price * quantity

            cur.execute(
                f'CREATE TABLE IF NOT EXISTS {emitent} (date TEXT, price INTEGER, quantity INTEGER, cost INTEGER)')
            cur.execute(f'INSERT INTO {emitent} (date, price, quantity, cost) VALUES (?, ?, ?, ?)',
                        (date, price, quantity, cost))

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
            answer = input('Are you sure want to sell?\nYes:Y\nNo:N\nAnswer: ')

            if answer.upper() == 'N':
                emitent = input('Enter emitent: ')
                ticker = input('Enter ticker: ')
            elif answer.upper() == 'Y':
                cur.execute('SELECT emitent FROM portfolio')
                print('#' * 35, '\nList of emitents from your portfolio:')
                for i, j in enumerate(cur.fetchall()):
                    print(f'{j[0]}: {i + 1}')
                name = int(input('Select shares to sell: '))
                cur.execute(f'SELECT emitent FROM portfolio WHERE rowid = {name}')
                emitent = cur.fetchall()[0][0]

            quantity_del = int(input('Number of shares sold: '))

            while quantity_del > 0:
                cur.execute(f'SELECT quantity FROM {emitent} WHERE rowid = (SELECT MIN(rowid) FROM {emitent})')
                quantity = cur.fetchall()[0][0]
                if quantity_del >= quantity:
                    cur.execute(f'DELETE FROM {emitent} WHERE rowid = (SELECT MIN(rowid) FROM {emitent})')
                else:
                    cur.execute(f'UPDATE {emitent} SET quantity = {quantity - quantity_del} WHERE rowid = (SELECT MIN(rowid) FROM {emitent})')
                quantity_del -= quantity
            cur.execute('UPDATE portfolio SET pos_quantity=?  WHERE emitent = ?', (get_pos_quantity(emitent), emitent))

        def get_show():
            cur.execute('SELECT * FROM portfolio')
            print('#' * 60, "\n", ' ' * 4, 'Emitent Ticker Quant Pos pr Pos cost Profit')
            for position in cur.fetchall():
                print(position)

        try:

            choice = int(input('Buy: 1\nSell: 2\nShow portfolio: 3\nEnter your chois: '))
            if choice == 1:
                get_buy()
            elif choice == 2:
                get_sell()
            elif choice == 3:
                get_show()
            else:
                print('Wrong enter')
        except ValueError:
            print('Wrong input')

        # cur.execute('''PRAGMA table_info(emmitent)''')
        # print(cur.fetchall())


if __name__ == '__main__':
    get_con()

