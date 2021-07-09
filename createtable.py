import sqlite3

conn = sqlite3.connect("portfolio.db")
conn.execute('DROP TABLE IF EXISTS PORTFOLIO')
conn.execute('''CREATE TABLE PORTFOLIO(
    ID INT PRIMARY KEY NOT NULL,
    SYMBOL TEXT NOT NULL, 
    STOCKNAME TEXT NOT NULL,
    UNITS INT NOT NULL,
    PRICE REAL NOT NULL,
    DATE TEXT NOT NULL)
''')

conn.close()
