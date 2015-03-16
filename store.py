import os
import sqlite3 
from config import *

class Database(object):

  def __init__(self, db_name='flashcard',table_name='flashcards'):
    self.db_name = db_name 
    self.db_file = DB_DIR + db_name + '.db'
    self.table_name = table_name
    db_exists =  os.path.exists(self.db_file)

    if db_exists:
      self.con = sqlite3.connect(self.db_file)

    else:
      ''' read schema file and execute with executescript
      which lets you run multiple SQL queries in a 
      single call 
      '''
      with open('flashcard_schema.sql') as f:
        schema_directives = f.read()
        self.con = sqlite3.connect(self.db_file)
        self.con.executescript(schema_directives)

    self.cur = self.con.cursor()

  def select(self, sql, safe_tuple=None):
    if safe_tuple:
      rows = self.con.execute(sql, safe_tuple)
    else: 
      rows = self.con.execute(sql)
    return [row for row in rows]

  def addCard(self, front, back):
    self.cur.execute('''INSERT INTO %s VALUES(?,?,?,?)''' % (self.table_name,),(None,front,back,0))
    self.con.commit()

  def insert(self, sql, safe_tuple):
    self.con.execute(sql, safe_tuple)
    self.con.commit()

  def update(self, sql, safe_tuple):
    self.con.execute(sql, safe_tuple)
    self.con.commit()

  def delete(self,sql, safe_tuple):
    self.con.execute(sql, safe_tuple)
    self.con.commit()

  def get_db_name(self):
    return self.db_name
