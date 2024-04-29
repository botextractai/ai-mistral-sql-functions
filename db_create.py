import sqlite3

connection_obj = sqlite3.connect('demo_sqlite.db')

cursor_obj = connection_obj.cursor()

connection_obj.execute("""CREATE TABLE CUSTOMERS(
    customer_id varchar(5),
    customer_name varchar(10)
);""")

connection_obj.execute(
    """INSERT INTO CUSTOMERS (customer_id,customer_name) VALUES ('C1001','Smith')""")
connection_obj.execute(
    """INSERT INTO CUSTOMERS (customer_id,customer_name) VALUES ('C1002','Johnson')""")
connection_obj.execute(
    """INSERT INTO CUSTOMERS (customer_id,customer_name) VALUES ('C1003','Williams')""")
connection_obj.execute(
    """INSERT INTO CUSTOMERS (customer_id,customer_name) VALUES ('C1004','Brown')""")
connection_obj.execute(
    """INSERT INTO CUSTOMERS (customer_id,customer_name) VALUES ('C1005','Jones')""")

connection_obj.commit()

connection_obj.execute("""CREATE TABLE PAYMENTS(
    customer_id varchar(5),
    payment_amount real
);""")

connection_obj.execute(
    """INSERT INTO PAYMENTS (customer_id,payment_amount) VALUES ('C1001',10.85)""")
connection_obj.execute(
    """INSERT INTO PAYMENTS (customer_id,payment_amount) VALUES ('C1002',23.41)""")
connection_obj.execute(
    """INSERT INTO PAYMENTS (customer_id,payment_amount) VALUES ('C1003',19.62)""")
connection_obj.execute(
    """INSERT INTO PAYMENTS (customer_id,payment_amount) VALUES ('C1004',48.17)""")
connection_obj.execute(
    """INSERT INTO PAYMENTS (customer_id,payment_amount) VALUES ('C1005',11.94)""")
connection_obj.execute(
    """INSERT INTO PAYMENTS (customer_id,payment_amount) VALUES ('C1001',34.29)""")
connection_obj.execute(
    """INSERT INTO PAYMENTS (customer_id,payment_amount) VALUES ('C1002',27.43)""")
connection_obj.execute(
    """INSERT INTO PAYMENTS (customer_id,payment_amount) VALUES ('C1003',44.98)""")
connection_obj.execute(
    """INSERT INTO PAYMENTS (customer_id,payment_amount) VALUES ('C1004',16.75)""")
connection_obj.execute(
    """INSERT INTO PAYMENTS (customer_id,payment_amount) VALUES ('C1005',30.12)""")

connection_obj.commit()

connection_obj.close()
