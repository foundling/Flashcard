import os
from config import *


def print_cardset(db):
  rows = db.select('select * from flashcards')
  for row in rows:
    print 'FRONT: ', row[1]
    print 'BACK: ', row[2] 
  

def last_opened_db():
  dbs = [DB_DIR + f for f in os.listdir(os.path.dirname(DB_DIR))]
  dbs_by_atime = sorted(dbs,key=os.path.getatime,reverse=True)
  last_opened = dbs_by_atime[0]
  return last_opened

def show_available_files(filepath, extension=''):
  '''
  documentation to be written
  '''
  files = [ (os.path.dirname(filepath) + '/' + f) for f in os.listdir(filepath)\
    if f.endswith(extension) and not f.startswith('.')]
  #for n, v in enumerate(files, start=1):
  #  print "({}) {}".format(n,os.path.basename(v))
  return files
   
def clean(filename):
  '''

  '''
  return filename.replace(' ','_')

def clear_screen():
  os.system('clear')

def db_exists(db_name, loc=None):
  if loc is None:
    loc = DB_DIR

  if db_name:
    return os.path.isfile(loc + '/' + db_name + '.db')

  else:
    print 'no filename passed'
    return None

def load_cards_into_memory(db):
  rows = db.select('''SELECT front, back FROM flashcards''')
  return [ (row[0],row[1]) for row in rows ]
 

# prompts or just prints if you pass it prompt = False
def prompt(text='', response=True, leading_newlines = 0, trailing_newlines = 0):

  if response:
    return raw_input(text).encode('utf-8')

  else:
    print text + '\n'
