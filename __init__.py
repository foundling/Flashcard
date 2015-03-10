#!/usr/bin/env python

# Flashcard
# Very simple text-based quiz-yourself application

import os, sys

from store import Database

APP_PATH = os.path.dirname(os.path.abspath(__file__))
APP_DATA_DIR = APP_PATH + '/data/'
PARSE_FILES_DIR = APP_DATA_DIR + 'parse_files/'
DB_PATH = APP_PATH + '/db'
DB_DIR = DB_PATH + '/'

def main_menu(CURRENT_CARD_SET = None):
  clear_screen()

  prompt('Please choose an Option from the Menu',False)
  if CURRENT_CARD_SET:
    prompt('current card set: %s\n' % (CURRENT_CARD_SET),False)
  choices = ['Create a New Card Set', 'Load Card Set', 'Add a Card to an Existing Card Set', 'Quiz yourself', 'Quit']
  print '\n'.join("({}) {}".format(n,v) for n,v in enumerate(choices,start=1))
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
 
  if error_msg:
    name = clean_filename(prompt(error_msg))
  else:
    name = clean_filename(prompt('Please Enter a Name for your new Flashcard Set:  '))

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
          response = prompt('Card Set %s created successfully. Do you want to add cards to your cardset now? [y/N]' % (name))
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

# PUT NEW CARDS INTO DB
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

def load_cards_from_file(db):
  clear_screen() 
  prompt('[ NOTE: Files to be parsed should be placed in %s ]' % (PARSE_FILES_DIR),False)
  prompt('AVAILABLE FILES: \n',False)
  available_parse_files = show_available_files(PARSE_FILES_DIR)
  print '\n'.join("({}) {}".format(n,v) for n,v in enumerate(available_parse_files))
  prompt('')

##
## Helper Functions
##

def show_available_files(filepath, extension=''):
  return [ f for f in os.listdir(filepath) if f.endswith(extension) ]

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
def prompt(text='',response=True):
  text = text.strip()
  if response:
    return raw_input(text)
  else:
    print text + '\n'

def handle(response):
  pass





def main():
  card_set = None
  while True:
    card_set = main_menu(CURRENT_CARD_SET=card_set)
    if card_set:
      card_set = os.path.basename(card_set).split('.db')[0].upper()
    

if __name__ == '__main__':
  main()
