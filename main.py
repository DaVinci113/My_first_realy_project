import sqlite3 as sq
import requests
from fake_useragent import UserAgent
from config import headers, cookies, params
import time


def get_con():
    with sq.connect('test.db') as con:
        print('#' * 35, '\nConnection complete...\n#' + '#' * 34)

        cur = con.cursor()

        def get_pos_cost(emitent):
            cur.execute(f'SELECT cost FROM {emitent}')
            cost = cur.fetchall()
            result = 0
            for _ in cost:
                result += int(_[0])
            return result

        def get_pos_quantity(emitent):
            cur.execute(f'SELECT quantity FROM {emitent}')
            quantity = cur.fetchall()
            result = 0
            for _ in quantity:
                result += int(_[0])
            return result

        def get_current_price(emitent):

            cur.execute(f'SELECT ticker FROM portfolio WHERE emitent = \'{emitent}\'')
            ticker = cur.fetchall()[0][0]
            useragent = UserAgent().random
            headers['User-Agent'] = useragent
            params['code'] = ticker
            response = requests.get(
                f'https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}.json',
                params=params,
                cookies=cookies,
                headers=headers
            ).json()

            time.sleep(1)

            for i in response['marketdata']['data']:
                if i[1] == 'TQBR':
                    return i[4]

        def get_pos_price(emitent):
            return get_pos_quantity(emitent) * get_current_price(emitent)

        def get_match(emitent):
            cur.execute('SELECT emitent FROM portfolio')
            res = cur.fetchall()
            return any(emitent in x for x in res)

        def get_profit(emitent):
            return get_pos_price(emitent) - get_pos_cost(emitent)

        def get_buy():

            cur.execute(
                'CREATE TABLE IF NOT EXISTS portfolio (emitent TEXT, ticker TEXT, pos_quantity INTEGER, pos_price INTEGER, pos_cost INTEGER, profit)')  # Создание таблицы portfolio

            cur.execute('SELECT * FROM portfolio')
            scan = cur.fetchall()
            if scan:

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

            else:
                emitent = input('Enter emitent: ')
                ticker = input('Enter ticker: ')

            date = input('Enter date: ')
            price = int(input('Enter price: '))
            quantity = int(input('Enter quantity: '))
            cost = price * quantity

            cur.execute(
                f'CREATE TABLE IF NOT EXISTS {emitent} (date TEXT, price INTEGER, quantity INTEGER, cost INTEGER)', ())
            cur.execute(f'INSERT INTO {emitent} (date, price, quantity, cost) VALUES (?, ?, ?, ?)',
                        (date, price, quantity, cost))

            if not get_match(emitent):
                cur.execute('INSERT INTO portfolio (emitent, ticker, pos_quantity, pos_price) VALUES (?, ?, ?, ?)',
                            (emitent, ticker, quantity, price))


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
                    cur.execute(
                        f'UPDATE {emitent} SET quantity = {quantity - quantity_del} WHERE rowid = (SELECT MIN(rowid) FROM {emitent})')
                quantity_del -= quantity
            cur.execute('UPDATE portfolio SET pos_quantity=?  WHERE emitent = ?', (get_pos_quantity(emitent), emitent))

        def get_show():
            cur.execute('SELECT * FROM portfolio')
            print('#' * 60, "\n", ' ' * 4, 'Emitent Ticker Quant Pos pr Pos cost Profit')
            for position in cur.fetchall():
                print(position)

        def get_update_data():
            cur.execute('SELECT emitent FROM portfolio')
            emitents_list = cur.fetchall()
            for emitent in emitents_list:
                emitent = emitent[0]
                cur_price = get_pos_price(emitent)
                print(emitent, ' - Updated')

                cur.execute('UPDATE portfolio SET pos_price=? WHERE emitent=?', (cur_price, emitent))

            delete_zero_quantity()

        def delete_zero_quantity():
            cur.execute('SELECT emitent FROM portfolio WHERE pos_quantity = 0')
            for i in cur.fetchall()[0]:
                cur.execute(f'DROP TABLE {i}')
            cur.execute('DELETE FROM portfolio WHERE pos_quantity=0')

        try:

            choice = int(input('Buy: 1\nSell: 2\nShow portfolio: 3\nUpdate data: 4\nYour choise: '))
            if choice == 1:
                get_buy()
            elif choice == 2:
                get_sell()
            elif choice == 3:
                get_show()
            elif choice == 4:
                get_update_data()
            else:
                print('Wrong enter')
        except ValueError:
            print('Wrong input')


if __name__ == '__main__':
    get_con()
