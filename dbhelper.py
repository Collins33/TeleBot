import sqlite3

class DBHelper:
#this method takes a database name as argument and connects to it
    def __init__(self,dbname="todo.sqlite"):
        self.dbname=dbname
        self.conn=sqlite3.connect(dbname)
#this method creates a table called items with column called description
    def setUp(self):
        stmt="CREATE TABLE IF NOT EXISTS items (description text)"
        self.conn.execute(stmt)
        self.conn.commit()

#method to add to the database
    def add_item(self,item_text):
        stmt="INSERT INTO items (description) VALUES (?)"
        args=(item_text, )
        self.conn.execute(stmt,args)
        self.conn.commit()
