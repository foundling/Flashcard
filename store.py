import os
import sqlite3 
import config

class Database(object):

  def __init__(self, dbfile='db/default.db'):
    db_exists =  os.path.exists(dbfile)
    if not db_exists:
      ''' read schema file and execute with executescript
      which lets you run multiple SQL queries in a 
      single call 
      '''
      print 'LOADING SCHEMA' 
      with open('flashcard_schema.sql','rt') as f:
        schema_directives = f.read()
        self.db = sqlite3.connect(dbfile)
        self.db.executescript(schema_directives)

    self.db_file = os.path.abspath(dbfile)
    self.db_name = os.path.basename(self.db_file).split('.db')[0]

  def get_db_name(self):
    return self.db_name
 


if __name__ == '__main__':
  db = Database('db/default.db')
