import psycopg2
from psycopg2 import IntegrityError
import mvc_exceptions as mvc_exc


def select_query(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def select_all(conn, table_name):
    cur = conn.cursor()
    cur.execute('SELECT * FROM "{}"'.format(table_name))
    return cur.fetchall()


def insert_one(conn, table_name, field_values):
    cur = conn.cursor()
    keys = field_values.keys()
    columns = ','.join(keys)
    values = ','.join(['%({})s'.format(k) for k in keys])
    insert = 'INSERT INTO "{}" ({}) values ({})'.format(table_name, columns, values)
    cur.mogrify(insert, field_values)

    cur.execute(insert, field_values)
    conn.commit()


def select_one(conn, table_name, key_name, key_value):
    cur = conn.cursor()
    cur.execute('SELECT * FROM "{}" WHERE {} = %s LIMIT 1'.format(table_name, key_name), (key_value,))
    result = cur.fetchone()
    if result is not None:
        return result
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read row with {} = "{}" because it\'s not stored in table "{}"'
                .format(key_name, key_value, table_name))


def update_one(conn, table_name, key_change, new_val, key, key_val):
    cur = conn.cursor()
    sql_check = 'SELECT EXISTS(SELECT 1 FROM "{}" WHERE {} = %s LIMIT 1)' \
        .format(table_name, key)
    cur.execute(sql_check, (key_val,))
    result = cur.fetchone()
    if result is not None:
        cur.execute('UPDATE "{}" Set {} = %s WHERE {} = %s;'.format(table_name, key_change, key), (new_val, key_val))
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t update {} = {} because it\'s not stored in table "{}"'
                .format(key, key_val, table_name))


def delete_one(conn, table_name, key_name, key_val):
    cur = conn.cursor()
    sql_check = 'SELECT EXISTS(SELECT 1 FROM "{}" WHERE {} = %s LIMIT 1)' \
        .format(table_name, key_name)
    cur.execute(sql_check, (key_val,))
    result = cur.fetchone()

    if result is not None:
        cur.execute('DELETE FROM "{}" WHERE {} = %s'.format(table_name, key_name), (key_val,))
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t delete {} = {} because it\'s not stored in table "{}"'
                .format(key_name, key_val, table_name))


def get_columns(conn, table_name):
    cur = conn.cursor()
    value = []
    cur.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS" \
                " WHERE TABLE_NAME = '{}'".format(table_name))
    for column in cur.fetchall():
        value.append(*column)
    return value


def check_for_present(conn, column_name, table_name):
    columns = get_columns(conn, table_name)
    if column_name not in columns:
        return False
    return True


def get_list_of_tables(con):
    cur = con.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public'")
    return [col[0] for col in cur.fetchall()]
    # for table in cur.fetchall():
    #     print(table)


def get_column_type(conn, table, column_name):
    cur = conn.cursor()
    cur.execute("SELECT column_name, data_type FROM information_schema.columns "
                "WHERE table_name = '{}'".format(table))

    for col in cur.fetchall():
        if column_name in col:
            return col[1]


def column_data(con, table_name, column_name):
    try:
        cur = con.cursor()
        cur.execute('SELECT {} FROM "{}"'.format(column_name, table_name))
        values = []
        for val in cur.fetchall():
            values.append(*val)
        return values
    except(psycopg2.DatabaseError, Exception) as error:
        print(error)


def auto_gen_int(con, max_val, rows_number):
    try:
        query = 'SELECT trunc(random()*{}+1)::int from generate_series(1,{})'.format(max_val, rows_number)
        print(query)
        cur = con.cursor()
        cur.execute(query)
        # numbers = [num[0] for num in cursor.fetchall()]
        return cur.fetchall()
    except(psycopg2.DatabaseError, Exception) as error:
        print(error)


def auto_gen_char(con, str_len, rows_number):
    try:
        part = 'chr(trunc(65 + random()*25)::int)'
        if str_len > 0:
            param = part + (' || ' + part) * (str_len - 1)

        query = 'SELECT {} from generate_series(1,{})'.format(param, rows_number)
        print(query)
        cur = con.cursor()
        cur.execute(query)
        return cur.fetchall()
    except(psycopg2.DatabaseError, Exception) as error:
        print(error)
