#!/usr/bin/env python

# Flashcard
# A text-based, quiz-yourself application
#
# Licensed under the GNU objective distro interactive license.
#

import os, sys

from store import Database

APP_PATH = os.path.dirname(os.path.abspath(__file__))
APP_DATA_DIR = APP_PATH + '/data/'
PARSE_FILES_DIR = APP_DATA_DIR + 'parse_files/'
DB_PATH = APP_PATH + '/db'
DB_DIR = DB_PATH + '/'

def main_menu(CURRENT_CARD_SET = None):

  clear_screen()
  header()
  prompt('Please Choose an Option from the Menu',False)

  if CURRENT_CARD_SET:
    prompt('current card set: %s\n' % (CURRENT_CARD_SET), False) # False means no return value

  #  Please choose an Option from the Menu
  
  #  (1) Create a New Card Set
  #  (2) Load Card Set
  #  (3) Add a Card to an Existing Card Set
  #  (4) Quiz yourself
  #  (5) Quit

  choices = ['Create a New Card Set', 'Load Card Set', 'Add a Card to an Existing Card Set', 'Quiz yourself\n\n. . . . . . .\n','Settings','Info','Quit']
  print '\n'.join("({}) {}".format(n,v) for n,v in enumerate(choices, start=1))
  response = prompt('',True)

  if response in ['1']:
    create_new_card_set() 

  if response in ['2']:
    card_set = load_card_set()
    return card_set

  if response in ['3']:
    add_to_existing_card_set()

  if response in ['3']:
    quiz_yourself()

  if response in ['q','Q','5']:
    sys.exit(0)
  
def create_new_card_set(error_msg=None):

  clear_screen()
  new_card_set_header()
 
  if error_msg:
    '''
    We prompt them with the error message. Prompt by default returns the user's response, 
    which is the filename, so we take that and clean it.
    '''
    name = clean_filename( prompt(error_msg) )

  else:
    name = clean_filename( prompt('Please Enter a NAME for your new Flashcard Set:',leading_newlines=5) )

  if name:

    if file_exists(name):
      error_msg = 'This file already exists. Please Choose Another Name:\n'
      create_new_card_set(error_msg)

    else:
      card_set_name = DB_DIR + name + '.db'
      with open(card_set_name, 'a+') as f:
        try:
          f.write('') # create file

        except IOError:
          print "Could Not Open The Requested Card Set. See Log for Details"

        else: 
          db = Database(DB_DIR + name + '.db')
          response = prompt('Card Set "%s" created successfully.\nAdd cards to your cardset now? [y/N]' % (name))

          if response in ['y','Y']:
            response = prompt('Do you want to add the cards \n(1) manually, or \n(2) or parse them from a structured file?')

            if response in ['1']:
              load_cards_manually(db) 

            if response in ['2']:
              load_cards_from_file(db)

          if response in ['n','N']:
            return

  else:
    error_msg = "ERROR: You didn't provide a valid name."
    create_new_card_set(error_msg)

# ACTIVATE CARD SET
def load_card_set():

  clear_screen()
  cardsets = [ (DB_DIR + f) for f in os.listdir(DB_PATH) if f.endswith('.db') ]
  cardsets.sort(key=os.path.getctime)

  if cardsets:
    prompt('Please Choose a Cardset:', False)
    print '\n'.join('({}) {}'.format(n,os.path.basename(v)) for n,v in enumerate(cardsets))  
    response = int(prompt())
    db = Database(cardsets[response])

    if db.db_name:
      CURRENT_CARD_SET = db.db_name
      prompt('Card Set Loaded!')
      return CURRENT_CARD_SET

  else:
    prompt('You have no Card Sets. Hit any Key to return to the main Menu')

# PUT NEW CARDS INTO DB, ONE BY ONE
def load_cards_manually(db):

  clear_screen() 
  front,back = None, None

  while True:
    prompt("Enter 'q' or 'Q' into either field to quit at any time",False)
    front = prompt("FRONT: ")

    if front in ['q','Q']:
      break

    back = prompt("BACK: ")

    if back in ['q','Q']:
      break

    card = [front, back]
    db.add_card_to_set(card)


# PARSE A FILE INTO CARDS
def load_cards_from_file(db):
  clear_screen() 
  prompt('[ NOTE: Files to be parsed should be placed in %s ]' % (PARSE_FILES_DIR),False)
  prompt('PLEASE CHOOSE FROM AVAILABLE FILES: \n',False)
  print show_available_files(PARSE_FILES_DIR)
  prompt('') 
  ## STOPPED HERE, need to get to the loading part
  ## FIX show_avail_files
  

##
## Helper Functions
##

def show_available_files(filepath, extension=''):
  files = [ (os.path.dirname(filepath) + '/' + f) for f in os.listdir(filepath)]
  for n, v in enumerate(files, start=1):
    print "({}) {}".format(n,os.path.basename(v))
    
    

def clean_filename(filename):
  return filename.replace(' ','_')

def add_to_existing_card_set():
  pass

def quiz_yourself():
  pass

def clear_screen():
  os.system('clear')

def file_exists(filename=None, loc=None):
  if loc is None:
    loc = APP_PATH + '/db'

  if filename:
    return os.path.isfile(loc + '/' + filename)

  else:
    print 'no filename passed' 
    return None

def perror(error=None):
  if error: print error
  

# prompts or just prints if you pass it prompt = False
def prompt(text='', response=True, leading_newlines = 0, trailing_newlines = 0):

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

def header():
  print '************************************************'
  print '*                                              *'
  print '*                  FLASHCARD                   *'
  print '*                                              *'
  print '*          Your Personal Quiz-Engine           *'
  print '*                                              *'
  print '*                                              *'
  print '*                                              *'
  print '*    System Requirements: inodes, 512MB RAM    *'
  print '*                                              *'
  print '************************************************'
  print ''

def new_card_set_header():
  print '************************************************'
  print '*                                              *'
  print '*                NEW CARD SET                  *'
  print '*                                              *'
  print '************************************************'
  print ''

  


def main():

  card_set = None

  while True:
    card_set = main_menu(CURRENT_CARD_SET=card_set)

    if card_set:
      card_set = os.path.basename(card_set).split('.db')[0].upper()


if __name__ == '__main__':
  main()
