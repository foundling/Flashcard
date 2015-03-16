import os
import sqlite3 
import config

class Database(object):

  def __init__(self, dbfile='db/default.db'):
    db_exists =  os.path.exists(dbfile)

    if db_exists:
      self.db = sqlite3.connect(dbfile)

    else:
      ''' read schema file and execute with executescript
      which lets you run multiple SQL queries in a 
      single call 
      '''
      print 'LOADING SCHEMA' 

      with open('flashcard_schema.sql','rt') as f:
        schema_directives = f.read()
        self.db = sqlite3.connect(dbfile)
        self.db.executescript(schema_directives)

    self.cur = self.db.cursor()
    self.db_file = os.path.abspath(dbfile)
    self.db_name = os.path.basename(self.db_file).split('.db')[0]

  def select(self, sql, safe_tuple=None):
    if safe_tuple:
      rows = self.db.execute(sql, safe_tuple)
    else: 
      rows = self.db.execute(sql)
    return [row for row in rows]

  def insert(self, sql, safe_tuple):
    self.db.execute(sql, safe_tuple)
    self.db.commit()

  def update(self, sql, safe_tuple):
    self.db.execute(sql, safe_tuple)
    self.db.commit()

  def delete(self,sql, safe_tuple):
    self.db.execute(sql, safe_tuple)
    self.db.commit()

  def get_db_name(self):
    return self.db_name
 


if __name__ == '__main__':
  db = Database('db/default.db')
