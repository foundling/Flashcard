import os
from config import *

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
  '''

  '''
  os.system('clear')

def db_exists(db_name, loc=None):
  '''

  '''
  if loc is None:
    loc = DB_PATH

  if db_name:
    return os.path.isfile(loc + '/' + db_name)

  else:
    print 'no filename passed'
    return None

def perror(error=None):
  '''

  '''
  if error: print error

# prompts or just prints if you pass it prompt = False
def prompt(text='', response=True, leading_newlines = 0, trailing_newlines = 0):
  '''

  '''

## add some logic in here to limit line lenght of text, inserting new lines at '.' before 80 char.

  # this func doesn't work
  def chain_newlines(count=1):
    newlines = ''
    for i in range(count):
        newlines += '\n'

  if leading_newlines:
    chain_newlines(leading_newlines)

  if trailing_newlines:
    chain_newlines(trailing_newlines)

  if response:
    chain_newlines(leading_newlines)
    return raw_input(text)

  else:
    chain_newlines(leading_newlines)
    print text + '\n'
    chain_newlines(trailing_newlines)
