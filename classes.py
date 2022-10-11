from tkinter import *
from tkinter import ttk
import sqlite3
from pprint import pprint as pp


class App(ttk.Frame):
    db_name = "products.sqlite"

    def __init__(self, window):
        super().__init__(window)
        window.title("Inventario v0.1")
        window.config(padx=20, pady=20)

        # Labels ############################################

        # Row 0
        self.actions_label = Label(text="Actions:")
        self.actions_label.grid(row=0, column=0, sticky="w")

        # Row 2
        self.product_label = Label(text="Product:")
        self.product_label.grid(row=2, column=0, padx=3, pady=5)
        self.quantity_label = Label(text="Quantity:")
        self.quantity_label.grid(row=2, column=1, padx=3, pady=5)

        # Row 4
        self.product_label2 = Label(text="Product:")
        self.product_label2.grid(row=4, column=0, padx=3, pady=5)
        self.quantity_label2 = Label(text="Quantity:")
        self.quantity_label2.grid(row=4, column=1, padx=3, pady=5)
        self.price_label = Label(text="Price:")
        self.price_label.grid(row=4, column=2, padx=3, pady=5)

        # Buttons ############################################

        # Row 1
        self.products_button = Button(text="Products", width=15, command=self.list_products)
        self.products_button.grid(row=1, column=0, padx=3)
        self.sales_button = Button(text="Sales", width=15, command=self.list_sales)
        self.sales_button.grid(row=1, column=1, padx=3)
        self.purchases_button = Button(text="Purchases", width=15, command=self.list_purchases)
        self.purchases_button.grid(row=1, column=2, padx=3)

        # Row 3
        self.sell_button = Button(text="Sell", width=15, command=self.sell_product)
        self.sell_button.grid(row=3, column=2, padx=3)
        self.buy_button = Button(text="Buy", width=15, command=self.buy_product)
        self.buy_button.grid(row=3, column=3, padx=3)

        # Row 6
        self.add_button = Button(text="Add", width=15, command=self.add_product)
        self.add_button.grid(row=6, column=3, padx=3)

        # Entries ############################################

        # Row 3
        self.product_entry = Entry(width=18)
        self.product_entry.grid(row=3, column=0, padx=3)
        self.quantity_entry = Entry(width=18)
        self.quantity_entry.grid(row=3, column=1, padx=3)

        # Row 6
        self.product_entry2 = Entry(width=18)
        self.product_entry2.grid(row=6, column=0, padx=3)
        self.quantity_entry2 = Entry(width=18)
        self.quantity_entry2.grid(row=6, column=1, padx=3)
        self.price_entry = Entry(width=18)
        self.price_entry.grid(row=6, column=2, padx=3)

    def add_product(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        parameters = (self.product_entry2.get().lower(),
                      self.quantity_entry2.get(),
                      self.price_entry.get(),
                      )

        if self.no_empty_fields(parameters):
            cursor.execute("INSERT INTO products VALUES (?, ?, ?)", parameters)
            conn.commit()
            conn.close()
            print("Item successfully added.")

    def sell_product(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        parameters = (self.product_entry.get().lower(),
                      self.quantity_entry.get(),
                      "s",
                      )

        if self.no_empty_fields(parameters):
            cursor.execute(f"UPDATE products SET stock = stock - {parameters[1]} WHERE product IN('{parameters[0]}')")
            cursor.execute("INSERT INTO transactions VALUES (?, ?, ?)", parameters)
            conn.commit()
            conn.close()
            print("Item sold.")

    def buy_product(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        parameters = (self.product_entry.get().lower(),
                      self.quantity_entry.get(),
                      "b",
                      )

        if self.no_empty_fields(parameters):
            cursor.execute(f"UPDATE products SET stock = stock + {parameters[1]} WHERE product IN('{parameters[0]}')")
            cursor.execute("INSERT INTO transactions VALUES (?, ?, ?)", parameters)
            conn.commit()
            conn.close()
            print("Item bought.")

    def list_products(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        pp(products)
        conn.close()

    def list_sales(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE type IN('s')")
        sales = cursor.fetchall()
        pp(sales, indent=2)
        conn.close()

    def list_purchases(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE type IN('b')")
        purchases = cursor.fetchall()
        pp(purchases, indent=2)
        conn.close()

    def no_empty_fields(self, params: tuple) -> bool:
        for param in params:
            if not len(param):
                return False

        return True
