import model, view


class Controller:
    def __init__(self):
        self.model = model.Model("127.0.0.1", "5432", "Human resources", "postgres", "letubu17")
        self.v = view.View()
        self.check_connection = 0
        if self.model.f == 1:
            self.v.print_massage(f"Successfully connected to database \"{self.model.database}\"")
            self.check_connection = 1
        else:
            self.v.print_massage(f"Cannot connect to database \"{self.model.database}\"")

    def disconnect(self):
        self.model.disconnect()
        self.v.print_massage(f"Successfully disconnected from database \"{self.model.database}\"")

    def read_table_by_name(self):
        self.v.print_massage_to_input("Which table do you want to see?: ")
        self.table = input()
        self.read_table(self.table)

    def read_table(self, table):
        self.data = self.model.read_table(table)
        if self.data is None:
            self.v.print_massage(f"Cannot read table \"{table}\"")
        else:
            self.v.print_massage(f'\nTable "{table}":')
            # self.v.print_massage("_"*70)
            self.v.print_table(self.data)
            # self.v.print_massage("_"*70)

    def read_database(self):
        self.read_table("department")
        self.read_table("Company")
        self.read_table("employee")
        self.read_table("project")

    def delete(self):
        self.v.print_massage_to_input("Which table do you want to delete data from?: ")
        self.table = input()
        self.v.print_massage_to_input("Enter the condition(attribute:value): ")
        self.cond = input()
        print('')
        self.f = self.model.delete(self.table, self.cond)
        if self.f:
            self.v.print_massage('Successfully deleted')
            print('')
        else:
            self.v.print_massage('Deleting is not successfull\n')

    def insert(self):
        self.v.print_massage_to_input("Which table do you want to write data to?: ")
        self.table = input()
        self.columns = self.model.get_columns(self.table)
        if self.columns is not False:
            self.values = []
            for i in self.columns:
                self.v.print_massage_to_input(f"Enter the value of attribute {i}: ")
                inp = input()
                self.values.append(inp)
            self.f = self.model.insert(self.table, self.values)
            print('')
            if self.f:
                self.v.print_massage('Successfully inserted\n')
            else:
                self.v.print_massage('Inserting is not successfull\n')
        else:
            self.v.print_massage('Inserting is not successfull\n')

    def update(self):
        self.table = input('Which table do you want to update data in?: ')
        self.attr = input('Enter the attribute of tuple you want to update(attribute:value): ')
        self.update_attr = input("Enter the name of attribute you want to update: ")
        self.new_value = input('Enter the new value: ')
        print('')
        self.f = self.model.update(self.table, self.attr, self.update_attr, self.new_value)
        if self.f:
            self.v.print_massage('Successfully updated\n')
        else:
            self.v.print_massage('Updating is not successfull\n')

    def del_table(self):
        self.table = input("Which table do you want to delete data from?: ")
        self.f = self.model.delete_table(self.table)
        if self.f:
            self.v.print_massage(f'Successfully deleted the data from the table "{self.table}"')
            print('')
        else:
            self.v.print_massage('Deleting is not successfull')
            print('')

    def generate(self):
        self.v.print_massage_to_input('Which table do you want to insert generated data in?: ')
        self.table = input()
        self.v.print_massage_to_input('Enter the biggest value of id in this table?: ')
        self.count1 = input()
        self.v.print_massage_to_input('How many tuples do you want to insert?: ')
        self.count2 = input()
        print('')
        self.f = self.model.generate(self.table, self.count1, self.count2)
        if self.f:
            self.v.print_massage('Successfully inserted\n')
        else:
            self.v.print_massage('Insertion is not successfull\n')

    def search_by_attr(self):
        self.v.print_massage_to_input("Enter the first table: ")
        self.table1 = input()
        self.v.print_massage_to_input("Enter the second table: ")
        self.table2 = input()
        self.v.print_massage_to_input("Enter the attribute you want to search: ")
        self.atrr = input()
        self.v.print_massage_to_input("Enter the value for the attribute: ")
        self.val = input()
        self.v.print_massage('\n')
        self.result = self.model.search_by_attr(self.table1,self.table2, self.atrr, self.val)
        if self.result == None:
            print('Cannot perform attribute search\n')
        else:
            self.v.print_table(self.result)

    def text_search(self):
        self.v.print_massage_to_input("Which table do you want to search data in?: ")
        self.table = input()
        self.v.print_massage_to_input("Enter the mode:\n1.Not word match\n2.Word match\n")
        self.mode = input()
        self.v.print_massage_to_input("Enter the words you want to search text by: ")
        self.word = input()
        self.f = self.model.text_search(self.mode, self.word, self.table)
        if self.f is None:
            self.v.print_massage("Cannot perform text search")
        else:
            self.v.print_table(self.f)


class Menu:
    inp = None

    def __init__(self):
        self.c = Controller()
        self.ask()

    def ask(self):
        if self.c.check_connection == 0:
            return 0
        else:
            self.c.v.print_massage("What do you want to do?: ")
            self.c.v.print_massage("1.To see database")
            self.c.v.print_massage("2.To see specific table")
            self.c.v.print_massage("3.To delete specific data from specific table")
            self.c.v.print_massage("4.To delete data from specific table")
            self.c.v.print_massage("5.To update specific data in specific table")
            self.c.v.print_massage("6.To insert data into specific table")
            self.c.v.print_massage("7.To insert random generated data into specific table")
            self.c.v.print_massage("8.To perform a attribute search")
            self.c.v.print_massage("9.To perform a text search")
            self.c.v.print_massage("10.Nothing")
            Menu.inp = input()
            self.case()

    def case(self):
        if Menu.inp == '1':
            self.c.read_database()
            self.ask()
        elif Menu.inp == '2':
            self.c.read_table_by_name()
            self.ask()
        elif Menu.inp == '3':
            self.c.delete()
            self.ask()
        elif Menu.inp == '4':
            self.c.del_table()
            self.ask()
        elif Menu.inp == '5':
            self.c.update()
            self.ask()
        elif Menu.inp == '6':
            self.c.insert()
            self.ask()
        elif Menu.inp == '7':
            self.c.generate()
            self.ask()
        elif Menu.inp == '8':
            self.c.search_by_attr()
            self.ask()
        elif Menu.inp == '9':
            self.c.text_search()
            self.ask()
            return
        elif Menu.inp == '10':
            self.c.disconnect()
        else:
            self.c.v.print_massage("TRY AGAIN")
            self.ask()


m = Menu()
