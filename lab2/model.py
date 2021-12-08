import psycopg2
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:12346789@localhost:5432/public',
                       echo=True)


class Model:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.__password = password
        self.f = 0
        try:
            self.connection = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
            self.cursor = self.connection.cursor()
            self.f = 1
        except Exception as e:
            print(e)

    @property
    def getter(self):
        return self.__password

    def disconnect(self):
        self.connection.close()
        self.cursor.close()

    def read_table(self, table):
        try:
            self.connection.commit()
            self.cursor.execute(f'SELECT * FROM public.{table}')
            self.rows = self.cursor.fetchall()
            self.columns = []
            for i in self.cursor.description:
                self.columns.append(list(i)[0])
            self.data = []
            self.data.append(self.rows)
            self.data.append(self.columns)
        # print(self.data)
        # return self.data
        except Exception as e:
            print(e)
            self.data = None
            return self.data
        return self.data

    def delete(self, table, cond):
        try:
            self.attr = cond.split(':')[0]
            self.value = cond.split(':')[1]
            self.connection.commit()
            self.cursor.execute(f'DELETE FROM public."{table}" WHERE {self.attr} = \'{self.value}\' ')
            self.connection.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def insert(self, table, values):
        try:
            self.val = tuple(values)
            self.connection.commit()
            self.cursor.execute(f"INSERT INTO public.\"{table}\"  VALUES {self.val}")
            self.connection.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def get_columns(self, table):
        try:
            self.connection.commit()
            self.cursor.execute(f'SELECT * FROM public."{table}"')
            self.rows = self.cursor.fetchall()
            self.columns = []
            for i in self.cursor.description:
                self.columns.append(list(i)[0])
            return self.columns
        except Exception as e:
            print(e)
            return False

    def update(self, table, attr, update_attr, new_value):
        try:
            self.attr = attr.split(':')[0]
            self.value = attr.split(':')[1]
            self.connection.commit()
            self.cursor.execute(
                f"UPDATE public.\"{table}\" SET {update_attr} = '{new_value}' WHERE {self.attr} = '{self.value}'")
            self.connection.commit()
        except Exception as e:
            print(a)
            return False
        return True

    def delete_table(self, table):
        try:
            self.connection.commit()
            self.cursor.execute(f'DELETE FROM public."{table}"')
            self.connection.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def generate(self, table, count1, count2):
        try:
            count1 = str(int(count1) + 1)
            count2 = str(int(count2)+int(count1))

            if table == "company":
                self.connection.commit()
                self.cursor.execute(f"""INSERT INTO public.company
                SELECT generate_series,
                chr(floor(65 + random()*25)::int) || 
                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                chr(floor(65 + random()*25)::int), 
                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                chr(floor(65 + random()*25)::int)
                FROM generate_series({count1},{count2}) """)
                self.connection.commit()
            elif table == 'project':
                self.connection.commit()
                self.cursor.execute(f"""INSERT INTO public.project
                                SELECT generate_series,
                                chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int), 
                                generate_series,
                                generate_series
                                FROM generate_series({count1},{count2}) """)
                self.connection.commit()
            elif table == 'employee':
                self.connection.commit()
                self.cursor.execute(f"""INSERT INTO public.employee
                                SELECT generate_series,
                                chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int), 
                                chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int), 
                                generate_series
                                FROM generate_series({count1},{count2}) """)
                self.connection.commit()
            elif table == 'department':
                self.connection.commit()
                self.cursor.execute(f"""INSERT INTO public.department
                                SELECT generate_series,
                                chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int) || chr(floor(65 + random()*25)::int) || 
                                chr(floor(65 + random()*25)::int),
                                1
                                FROM generate_series({count1},{count2}) """)
                self.connection.commit()
            else:
                print("Such table doesn't exist")
        except Exception as e:
            print(e)
            return False
        return True

    def search_by_attr(self, table1, table2, attr, value):
        try:
            self.connection.commit()
            self.cursor.execute(f"""SELECT * FROM public.{table1} as first INNER JOIN public.{table2} as second on first.{attr} = second.{attr} WHERE {value}""")

            self.rows = self.cursor.fetchall()
            self.columns = []
            for i in self.cursor.description:
                self.columns.append(list(i)[0])
            self.data = []
            self.data.append(self.rows)
            self.data.append(self.columns)
            return self.data
        except Exception as e:
            print(e)
            return None

    def text_search(self, mode, word, table):
        self.connection.commit()
        try:
            if mode == '1':
                self.words = word.split()
                self.words = '|'.join(self.words)
                self.cursor.execute(
                    f'select * from public."{table}" where not (to_tsvector(name) @@ to_tsquery(\'{self.words}\'))')
            elif mode == '2':
                self.words = word.split()
                self.words = '&'.join(self.words)
                self.cursor.execute(
                    f'select * from public."{table}" where (to_tsvector(name) @@ to_tsquery(\'{self.words}\'))')
            else:
                return None
            self.rows = self.cursor.fetchall()
            self.columns = []
            for i in self.cursor.description:
                self.columns.append(list(i)[0])
            self.data = []
            self.data.append(self.rows)
            self.data.append(self.columns)
        except Exception as e:
            print(e)
            self.data = None
            return self.data
        return self.data







