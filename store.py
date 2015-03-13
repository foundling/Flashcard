import os, sys
import config

class Database(object):

  db_dir = config.DB_DIR 
  suffix = '.db'

  def __init__(self,db_name='default',DELIM='#'):
    self.DELIM = DELIM
    self.db_file_path = self.db_dir + db_name + self.suffix 
    self.db_name = db_name
    self.cards = None 

  def add_card_to_set(self, card):
    with open(self.db_file_path,"a+") as _db:
      _db.write(self.DELIM.join(card) + '\n')

  def parse_file(self,filename=None):
    '''
    returns a list of front,back tuples
    '''
    words = []
    with open(filename,'r') as fh:
      for line in fh.readlines():
        front,back = line.split(self.DELIM) 
        words.append((front,back.strip()))
    return words

  def load_card_set_as_cards(self):
    with open(self.db_file_path) as _db:
      lines = _db.readlines() 
      self.cards = [i.strip().split('#') for i in lines]

