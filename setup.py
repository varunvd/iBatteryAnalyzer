import sqlite3
conn=sqlite3.connect('Battery.db')
c=conn.cursor()
c.execute('''CREATE TABLE battery (sl integer, date text, status text) ''')
conn.commit()
