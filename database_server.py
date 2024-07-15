import sqlite3
import requests


class Database:
    def __init__(self, url):
        r = requests.get(f'{url}/api/check_connection')
        print(r.text)
        self.url = url
        

    def new_write(self, data, table):
        write_data = {
            'table': table,
            'data': data
        }
        r = requests.post(f'{self.url}/api/new_write', json=write_data)

        print(r.text)

    def update_data(self, data: dict(), filters: dict() = None, table=None):
        '''
        обновление данных в бд

        data - словарь в формате <колонна>:<значение> (можно несколько)
        id - обновление произойдет только у определенного пользователя, если None - у всех
        table - таблица, в которой произойдет обновление данных
        '''

        update_data = {
            'table': table,
            'filters': filters,
            'data': data
        }

        r = requests.post(f'{self.url}/api/update_data', json=update_data)

        print(r.text)

    def get_data(self, filters: dict() = None, table=None):
        '''
        Получает данные из базы данных и возвращает список словарей, где ключи - это названия колонок таблицы.
    
        filters - фильтры для поиска в формате {колонка: значение}.
        table - имя таблицы, из которой будут получены данные.
        '''

        get_data = {
            'table': table,
            'filters': filters
        }

        r = requests.post(f'{self.url}/api/get_data', json=get_data)

        return r.json()

    def delete(self, table, filters: dict() = dict()):
        delete_data = {
            'table': table,
            'filters': filters
        }

        r = requests.post(f'{self.url}/api/delete', json=delete_data)

        print(r.text)