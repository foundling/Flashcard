import os, sys
import config

class Database(object):

  db_dir = config.DB_DIR 
  suffix = '.db'

  def __init__(self,db_name='default',DELIM='#'):
    self.DELIM = DELIM
    self.db_file_name = self.db_dir + db_name + self.suffix 
    self.db_name = db_name

  def add_card_to_set(self, card):
    with open(self.db_name,"a+") as _db:
      _db.write(self.DELIM.join(card) + '\n')

  def parse_file(self,filename):
    '''
    returns a list of front,back tuples
    '''
    words = []
    with open(filename,'r') as fh:
      for line in fh.readlines():
        front,back = line.split(self.DELIM) 
        words.append((front,back.strip()))
    return words

#db = Database()
#print db.parse_file('testfile')
