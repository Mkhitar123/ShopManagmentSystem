import sqlite3 as sql
import tkinter as tk
try:
    with sql.connect("DB.db") as conn:
        print(f"Connected by using sqlite {sql.sqlite_version} version.")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS products (
                       bar_code TEXT PRIMARY KEY,
                       product_name TEXT NOT NULL,
                       product_type TEXT NOT NULL,
                       product_price TEXT NOT NULL,
                       product_mass TEXT NOT NULL,
                       product_quantity TEXT NOT NULL,
                       product_cost_price TEXT NOT NULL
                       );""")
        conn.commit()

        def insert_product(product_entres):
            sq = '''INSERT OR IGNORE INTO products(bar_code,product_name,product_type,product_price,product_mass,product_quantity,product_cost_price)
            VALUES(?,?,?,?,?,?,?)'''
            cur = conn.cursor()
            product=tuple( val.get() for val in product_entres)
            #print(product)
            for  t in product_entres: t.delete(0,tk.END)
            cur.execute(sq,product)
            conn.commit()
            return cur.lastrowid
        
        def update_product_db(product_entres):
            print(product_entres)
            sq  = '''UPDATE products SET product_name=?, product_type=?, product_price=?, product_mass=?, product_quantity=?, product_cost_price=? WHERE bar_code = ?'''
            cur = conn.cursor()
            cur.execute(sq,product_entres)
            conn.commit()
            return cur.lastrowid
        
        def update_product_after_sell(bar_code,mass,quantity):
            val = (mass,quantity,bar_code)
            sq  = '''UPDATE products SET product_mass=?, product_quantity=? WHERE bar_code = ?'''
            cur = conn.cursor()
            cur.execute(sq,val)
            conn.commit()
            return cur.lastrowid
        
        def search_product(product_entres):
            bar_code = str(product_entres[0].get())
            sq = '''SELECT * FROM products WHERE bar_code LIKE ?'''
            cur = conn.cursor()
            cur.execute(sq,[bar_code])
            ret = cur.fetchall()
            if ret:
                return ret
            else:
                return None

        def delete_product(product_entres):
            bar_code = str(product_entres[0].get())
            sq = '''DELETE FROM products WHERE bar_code LIKE ?'''
            cur = conn.cursor()
            cur.execute(sq,[bar_code])
            for  t in product_entres: t.delete(0,tk.END)
            conn.commit()
            return cur.lastrowid
        
except sql.OperationalError as e:
    print("Failed to open database:", e)

