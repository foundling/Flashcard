import os, sys


class Database(object):
  def __init__(self,db_name=None,DELIM='#'):

    self.DELIM = DELIM

    if db_name is not None:
      open(db_name,'a+')
      self.db_name = db_name

  def add_card_to_set(self, card):
    with open(self.db_name,"a+") as _db:
      _db.write(self.DELIM.join(card) + '\n')

  def parse_file(self,filename):
    words = []
    with open(filename,'r') as fh:
      for line in fh.readlines():
        front,back = line.split(self.DELIM) 
        words.append((front,back.strip()))
    return words

db = Database()
print db.parse_file('testfile')
