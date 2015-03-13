#!/usr/bin/env python

# Flashcard
# A text-based, quiz-yourself application
#
# Licensed under the GNU objective distro interactive license.
#

import os, sys

import headers
from config import *
from store import Database

def main_menu(db):

  clear_screen()
  headers.main_header()
  prompt('Current Card Set: %s' % (db.db_name.upper()),False)
  prompt('Please Choose an Option from the Menu',False)

  choices = [ 'Create a New Card Set', 
              'Load Card Set',
              'Show Current Card Set',
              'Add a Card to an Existing Card Set', 
              'Quiz Yourself\n',
              'Info',
              'Settings', 
              'Quit'
             ]

  response = prompt('\n'.join("({}) {}".format(n,v) for n,v in enumerate(choices, start=1)) + '\n')

  if response in ['1']:
    create_new_card_set() 

  if response in ['2']:
    return load_card_set()

  if response in ['3']:
    show_current_card_set(db)

  if response in ['4']:
    add_to_existing_card_set()

  if response in ['3']:
    quiz_yourself()

  if response in ['q','Q','5']:
    sys.exit(0)
  
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
          response = prompt('\nCard Set "%s" created successfully.\n\nAdd cards to your cardset now? [y/N]: ' % (name))

          if response in ['y','Y']:
            response = prompt('\nDo you want to add the cards\n\n(1) manually, or \n(2) or parse them from a structured file? ')

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

##
## Helper Functions
##

def show_available_files(filepath, extension=''):
  files = [ (os.path.dirname(filepath) + '/' + f) for f in os.listdir(filepath) if f.endswith(extension)]
  #for n, v in enumerate(files, start=1):
  #  print "({}) {}".format(n,os.path.basename(v))
  return files
    
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


def main():

  db = Database() 
  db.load_card_set_as_cards()
  while True:
    main_menu(db)


if __name__ == '__main__':
  main()
