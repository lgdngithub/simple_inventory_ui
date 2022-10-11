# import sqlite3
#
# conn = sqlite3.connect("products.sqlite")
# cursor = conn.cursor()

# cursor.execute("""CREATE TABLE products
# (
#   product varchar(250) NOT NULL UNIQUE,
#   stock INTEGER NOT NULL,
#   price FLOAT NOT NULL
# )
# """)

# cursor.execute("""CREATE TABLE transactions
# (
# product varchar(250) NOT NULL,
# quantity INTEGER NOT NULL,
# type char(1) NOT NULL
# )
# """)

# conn.commit()
