import psycopg2 as psycopg2
import postgresql_backend
from time_decor import timer


class ModelPostgreSQL(object):

    def __init__(self):
        self._connection = psycopg2.connect(database='delivery', user='postgres',
                                            password='qwerty', host='localhost')

    @property
    def connection(self):
        return self._connection

    @timer
    def select_query(self, query):
        return postgresql_backend.select_query(self.connection, query)

    def create_item(self, table_name, field_values):
        return postgresql_backend.insert_one(self.connection, table_name, field_values)

    def read_item(self, table_name, key_name, key_val):
        return postgresql_backend.select_one(self.connection, table_name, key_name, key_val)

    def read_items(self, table_name):
        return postgresql_backend.select_all(self.connection, table_name)

    def update_item(self, table_name, key_change, new_val, key_name, key_val):
        return postgresql_backend.update_one(self.connection, table_name, key_change, new_val, key_name, key_val)

    def delete_item(self, table_name, key_name, key_val):
        return postgresql_backend.delete_one(self.connection, table_name, key_name, key_val)

    def get_columns(self, table_name):
        return postgresql_backend.get_columns(self.connection, table_name)

    def check_for_present(self, column_name, table_name):
        return postgresql_backend.check_for_present(self.connection, column_name, table_name)

    def get_list_of_tables(self):
        return postgresql_backend.get_list_of_tables(self.connection)

    def get_column_type(self, table, column_name):
        return postgresql_backend.get_column_type(self.connection, table, column_name)

    def column_data(self, table_name, column_name):
        return postgresql_backend.column_data(self.connection, table_name, column_name)

    def auto_gen_int(self, rows_number, max_val):
        return postgresql_backend.auto_gen_int(self.connection, max_val, rows_number)

    def auto_gen_char(self, rows_number, str_len):
        return postgresql_backend.auto_gen_char(self.connection, str_len, rows_number)

    def __del__(self):
        self.connection.close()

