import sqlite3

class DBHelper:
#this method takes a database name as argument and connects to it
    def __init__(self,dbname="todo.sqlite"):
        self.dbname=dbname
        self.conn=sqlite3.connect(dbname)
#this method creates a table called items with column called description
    def setUp(self):
        print("creating table")
        stmt="CREATE TABLE IF NOT EXISTS items (description text,owner text)"
        self.conn.execute(stmt)
        self.conn.commit()

#method to add to the database
    def add_item(self,item_text,owner):
        stmt="INSERT INTO items (description,owner) VALUES (?,?)"
        args=(item_text,owner)
        self.conn.execute(stmt,args)
        self.conn.commit()
#method to delete from the database
    def delete_item(self,item_text,owner):
        stmt="DELETE FROM items WHERE description =(?) and owner = (?)"
        args=(item_text,owner)
        self.conn.execute(stmt,args)
        self.conn.commit()
        
#method to return list of items from the db
    def get_items(self, owner):
       stmt = "SELECT description FROM items WHERE owner = (?)"
       args = (owner, )
       return [x[0] for x in self.conn.execute(stmt, args)]
