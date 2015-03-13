#!/usr/bin/env python

# Flashcard
# A text-based, quiz-yourself application
#
# Licensed under the GNU objective distro interactive license.
#

import os, sys

import headers
from config import *
from helper_funcs import *
from store import Database

def main_menu(db):

  clear_screen()
  headers.main_header()
  prompt('Current Card Set: %s' % (db.db_name.upper()),False)
  prompt('Please Choose an Option from the Menu',False)

  choices = [ 'Create a New Card Set', 
              'Load Card Set',
              'Show Current Card Set',
              'Add a Cards to Current Card Set', 
              'Quiz Yourself\n',
              'Info',
              'Configuration & Settings', 
              'Quit'
             ]

  response = prompt('\n'.join("({}) {}".format(n,v) for n,v in enumerate(choices, start=1)) + '\n')

  if response in ['1']:
    return create_new_card_set() # returns a re-initialized db object

  if response in ['2']:
    return load_card_set() # returns a re-initialized db object

  if response in ['3']:
    show_current_card_set(db)

  if response in ['4']:
    add_to_existing_card_set(db)

  if response in ['3']:
    quiz_yourself(db)

  if response in ['q','Q']:
    sys.exit(0)

  else:
    main_menu(db)
  
def create_new_card_set(error_msg=None):

  clear_screen()
  headers.new_card_set_header()
 
  if error_msg:
    '''
    We prompt them with the error message. Prompt by default returns the user's response, 
    which is the filename, so we take that and clean it.
    '''
    name = clean_filename( prompt(error_msg) )

  else:
    name = clean_filename( prompt('Please Enter a NAME for your new Flashcard Set:\n\n') )

  if name:
    card_set_name = name + '.db'

    if file_exists(card_set_name): # file_exists default dir is db/
      error_msg = 'This file already exists. Please Choose Another Name:\n'
      create_new_card_set(error_msg)

    else:
      with open(DB_DIR + card_set_name,'a+') as f:
        f.write('')

      db = Database(name)
      response = prompt('\nCard Set "%s" created successfully.\n\nAdd cards to your cardset now? [y/N]: ' % (name))

      if response in ['y','Y']:
        response = prompt('\nDo you want to add the cards\n\n(1) manually, or \n(2) or parse them from a structured file? ')

      if response in ['1']:
        load_cards_manually(db) 

      if response in ['2']:
        load_cards_from_file(db)
              
      if response in ['n','N']:
        return
      return db

  else:
    error_msg = "ERROR: You didn't provide a valid name."
    create_new_card_set(error_msg)

# ACTIVATE CARD SET
def load_card_set(error_msg=None):
  # should return a new database

  clear_screen()
  cardsets = [ (DB_DIR + f) for f in os.listdir(DB_PATH) if f.endswith('.db') ]
  cardsets.sort(key=os.path.getctime)

  if cardsets:
    prompt('Please Choose a Cardset:', False)
    print '\n'.join('({}) {}'.format(n,os.path.basename(v)) for n,v in enumerate(cardsets,start=1))  
    response = int(prompt())
    if not response:
      load_card_set('Please enter a valid number in the range of %d and %d' % (1,len(cardsets)))
    response_index = response - 1
    cardset_name = os.path.basename(cardsets[response_index]).split('.db')[0]
    db = Database(cardset_name)
  
    if db.db_name:
      prompt('Card Set Loaded!')
      return db

  else:
    prompt('You have no Card Sets. Hit any Key to return to the main Menu')


# PUT NEW CARDS INTO DB, ONE BY ONE
def load_cards_manually(db):

  clear_screen() 
  headers.load_cards_header()
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
  available_files = show_available_files(PARSE_FILES_DIR)

  if available_files:
    prompt('PLEASE CHOOSE FROM AVAILABLE FILES: \n',False)
    for n,v in enumerate(available_files):
      print "({}) {}".format(n,os.path.basename(v))
    
    response = prompt('Your choice: ') 

    try:
      index = int(response.strip())
      available_files[index]

    except IndexError:
      print 'not a valid choice'
      load_cards_from_file(db) 

  else:
    headers.error_header('ERROR: No files available for parsing.  \nMake sure to place your parsable files in:\n [ %s ].  \nPress any key to return to the MAIN MENU.')
    prompt('\nERROR: No files available for parsing.\n\nMake sure to place your parsable files in:\n\n### %s ###.\n\nPress any key to return to the MAIN MENU.' % (os.path.dirname(PARSE_FILES_DIR)))
    

def show_current_card_set(db=None):
  clear_screen()
  headers.current_card_set_header()
  prompt("Card Set: %s" % db.db_name.upper(),False)
  for f,b in [i for i in db.cards]:
    print f, ": ",b 
  prompt('\nHit Any Key to Return to the Main Menu')

def add_to_existing_card_set(db):
  pass 

def main():
  db = Database() ## init with default database 
  db.load_card_set_as_cards() ## load cards from default in  memory
  while True:
    new_db = main_menu(db)

    if new_db is not None:  
      db = new_db # rebind db to the newly returned database object
      db.load_card_set_as_cards() # load cards into memory

def quiz_yourself(db):
  pass

if __name__ == '__main__':
  main()
