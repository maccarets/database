from tabulate import tabulate

class View:
    def print_table(self, data):
    	self.middle = len(data[1])
    	print(tabulate(data[0], headers = data[1], tablefmt = 'fancy_grid'), '\n')
    def print_massage(self, massege):
        print(massege)

    def print_massage_to_input(self,massage):
    	print(massage , end = '')

