import psycopg2

from controller import Controller
from model import ModelPostgreSQL
from view import View


def task1(ctrl):
    print("List of tables")
    print(ctrl.get_list_of_tables())
    print("Enter table name")
    table_name = input()
    columns = ctrl.get_columns(table_name)
    if columns is None:
        return
    print('Columns list')
    print(ctrl.get_columns(table_name))

    ins_values = {}
    print("Insertion")
    for col in columns:
        col_type = ctrl.get_column_type(table_name, col)
        print('Please enter value of column {}, type = {}'.format(col, col_type))
        val = input()
        ins_values[col] = val
    ctrl.insert_item(table_name, ins_values)
    ctrl.show_items(table_name)

    print("Updating")
    print('Please enter key name of row to update')
    key_name = input()
    while ctrl.check_for_present(key_name, table_name) is False:
        print('Column name not found. Try again')
        key_name = input()
    print('Please enter key value')
    key_val = input()

    print('Enter column name to change')
    column_name = input()
    while ctrl.check_for_present(column_name, table_name) is False:
        print('Column name not found. Try again')
        column_name = input()

    col_type = ctrl.get_column_type(table_name, column_name)
    print('Please enter value of column {}, type = {}'.format(column_name, col_type))
    column_value = input()

    ctrl.update_item(table_name, column_name, column_value, key_name, key_val)

    print("Deleting")
    print('Enter column name')
    column_name = input()
    while ctrl.check_for_present(column_name, table_name) is False:
        print('Column name not found. Try again')
        column_name = input()
    col_type = ctrl.get_column_type(table_name, column_name)
    print('Please enter value of column {}, type = {}'.format(column_name, col_type))
    column_value = input()
    ctrl.delete_item(table_name, column_name, column_value)


def task2(ctrl):
    print("Enter table name")
    table_name = input()
    columns = ctrl.get_columns(table_name)
    if columns is None:
        return

    print("Enter number of rows to generate")
    rows_number = int(input())

    print("Enter max number")
    max_val = int(input())
    print("Enter string length")
    str_len = int(input())

    columns_type = [ctrl.get_column_type(table_name, col) for col in columns]
    print(columns_type)

    elements = []
    for i, column in enumerate(columns):

        if columns_type[i] == 'text':
            val = ctrl.auto_gen_char(rows_number, str_len)
        else:
            val = ctrl.auto_gen_int(rows_number, max_val)
        elements.append(val)

    for j in range(rows_number):
        item = []
        for k in range(len(columns)):
            item.append(elements[k][j])
        values = dict(zip(columns, item))
        try:
            ctrl.model.create_item(table_name,  values)
        except (psycopg2.DatabaseError, Exception) as error:
            pass


def task3(ctrl):

    print('query #1')
    print('Enter phone number template')
    phone = input()
    print('Enter dish 1')
    dish1 = input()
    print('Enter dish 2')
    dish2 = input()

    ctrl.search1(phone, dish1, dish2)

    print()
    print('query #2')
    print('Enter bigger then condition number')
    num = input()
    print('Enter characters that dish starts')
    dish_start = input()
    print('Enter phone number of restaurant starts')
    res_start = input()

    ctrl.search2(num, dish_start, res_start)

    print()
    print('query #3')
    print('Enter date after which orders were made')
    date_after = input()
    print('Enter min value of dishes which were ordered ')
    dish_min = input()
    print('Enter max value of dishes which were ordered')
    dish_max = input()
    print('Enter letter which person name contains')
    letter = input()
    ctrl.search3(date_after, dish_min, dish_max, letter)


def menu():
    print("Enter number of action")
    print("1. Task #1")
    print("2. Task #2")
    print("3. Task #3")
    print("4. Exit")


if __name__ == '__main__':
    c = Controller(ModelPostgreSQL(), View())

    task = 0
    while task != '4':
        menu()
        task = input()
        if task == '1':
            task1(c)
        elif task == '2':
            task2(c)
        elif task == '3':
            task3(c)
