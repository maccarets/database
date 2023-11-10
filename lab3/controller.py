 import psycopg2

import mvc_exceptions as mvc_exc

fdgbvdxfачс тм м
class Controller(object):gycfhgnfvbcfv

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self, table_name, bullet_points=False):
        items = self.model.read_items(table_name)

        if bullet_points:
            self.view.show_bullet_point_list(table_name, items)
        else:
            self.view.show_number_point_list(table_name, items)

    def insert_item(self, table_name, field_values):
        try:
            self.model.create_item(table_name, field_values)
            self.view.display_item_stored(table_name, field_values)
        except mvc_exc.ItemAlreadyStored as e:
            self.view.display_item_already_stored_error(table_name, e)
        except psycopg2.Error as e:
            self.model.connection.rollback()
            print('Insert error. \nType: {} \nText: {}'.format(type(e), e))

    def update_item(self, table_name, key_change, new_val, key_name, key_val):
        try:
            old_item = self.model.read_item(table_name, key_name, key_val)
            self.model.update_item(table_name, key_change, new_val, key_name, key_val)
            new_item = self.model.read_item(table_name, key_name, key_val)
            self.view.display_item_updated(table_name, new_item, old_item)
        except mvc_exc.ItemNotStored as e:
            self.view.display_item_not_yet_stored_error(key_val, table_name, e)
        except psycopg2.Error as e:
            self.model.connection.rollback()
            print('Update error. \nType: {} \nText: {}'.format(type(e), e))

    def delete_item(self, table_name, key_name, key_val):
        try:
            self.model.delete_item(table_name, key_name, key_val)
            self.view.display_item_deletion(table_name, key_val)
        except mvc_exc.ItemNotStored as e:
            self.view.display_item_not_yet_stored_error(key_val, table_name, e)
        except psycopg2.Error as e:
            self.model.connection.rollback()
            print('Delete error. \nType: {} \nText: {}'.format(type(e), e))

    def get_columns(self, table_name):
        return self.model.get_columns(table_name)

    def check_for_present(self, column_name, table_name):
        return self.model.check_for_present(column_name, table_name)

    def get_list_of_tables(self):
        return self.model.get_list_of_tables()

    def get_column_type(self, table, column_name):
        return self.model.get_column_type(table, column_name)

    def column_data(self, table_name, column_name):
        return self.model.column_data(table_name, column_name)

    def auto_gen_int(self, rows_number, max_val=100):
        return self.model.auto_gen_int(rows_number, max_val)

    def auto_gen_char(self, rows_number, str_len=5):
        return self.model.auto_gen_char(rows_number, str_len)

    def search1(self, search_tmpl, dish1, dish2):
        sql = 'SELECT title_rest, numb_rest, num_license ' \
               'FROM "Restaurant" ' \
               'JOIN "License" ' \
               'ON "Restaurant".id_restaurant = "License".id_restaurant ' \
               'JOIN "Dish" ' \
               'ON "Restaurant".id_restaurant = "Dish".id_restaurant ' \
               'WHERE numb_rest LIKE \'{}%\' '\
               'AND (name_dish = \'{}\' OR name_dish = \'{}\')'.format(search_tmpl, dish1, dish2)

        res = self.model.select_query(sql)
        print("title_rest, numb_rest, num_license")
        print(res)

    def search2(self, dish_amount, name_dish_start, numb_start):
        sql = 'SELECT name_dish, title_rest, numb_rest FROM ' \
              '(SELECT id_dish, count(id_dish) AS dish_cnt FROM "Order/Dish" ' \
              'GROUP BY id_dish) AS "DishCont" ' \
              'JOIN "Dish" ' \
              'ON "Dish".id_dish = "DishCont".id_dish ' \
              'JOIN "Restaurant" ' \
              'ON "Restaurant".id_restaurant = "Dish".id_restaurant ' \
              'WHERE dish_cnt > {} ' \
              'AND name_dish LIKE \'{}%\' ' \
              'AND numb_rest LIKE \'{}%\''.format(dish_amount, name_dish_start, numb_start)
        res = self.model.select_query(sql)
        print("name_dish, title_rest, numb_rest")
        print(res)

    def search3(self, after_date, dish_cnt_min, dish_cnt_max, name_contains):
        sql = 'SELECT dish_cnt, name_person, adress_person FROM ' \
              '(SELECT count(id_dish) AS dish_cnt, name_person, "Person".id_person, adress_person ' \
              'FROM "Person" ' \
              'JOIN "Order" ON "Order".id_person = "Person".id_person ' \
              'JOIN "Order/Dish" ON "Order/Dish".id_order = "Order".id_order ' \
              'WHERE date_order > \'{}\' ' \
              'GROUP BY name_person, "Person".id_person) AS "DishCount" ' \
              'WHERE "DishCount".dish_cnt BETWEEN {} AND {} ' \
              'AND name_person ILIKE \'%{}%\''.format(after_date, dish_cnt_min, dish_cnt_max, name_contains)
        res = self.model.select_query(sql)
        print("dish_cnt, name_person, adress_person")
        print(res)

