import sqlite3 as sql

con = sql.connect('kabish.db')
if con:
    print("connected")
else:
    print("No")

cur = con.cursor()
cur.execute('SELECT * FROM POSITION;')
rows = cur.fetchall()
for row in rows:
    print(row)

cur.close()
con.close()