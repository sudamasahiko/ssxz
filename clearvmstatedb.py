import sqlite3
conn = sqlite3.connect('vmstate.db')
cur = conn.cursor()
sql = 'DROP TABLE vmstate'
cur.execute(sql)
conn.commit()
sql = 'CREATE TABLE vmstate(name TEXT, ip TEXT)'
cur.execute(sql)
conn.commit()
conn.close()