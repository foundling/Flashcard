#!/usr/bin/env python
# -*- coding: <encoding name> -*-

# Flashcard
#
# A text-based, quiz-yourself application
# copyright (c) 2015 by Alex Ramsdell

import os, sys

from config import *
from store import Database
from quiz import QuizEngine
from helper_funcs import *
import headers

def main_menu(db):
  clear_screen()
  prompt('Current Card Set: %s' % (db.db_name.upper()),False)
  prompt('Please Choose an Option from the Menu',False)

  choices = [ 'Create a New Card Set', 
              'Load Card Set',
              'Show Current Card Set',
              'Add Cards to Current Card Set', 
              'Quiz Yourself\n',
              'Info',
              'Configuration & Settings', 
              'Quit'
             ]

  response = prompt('\n'.join("({}) {}".format(n,v) for n,v in enumerate(choices, start=1)) + '\n')

  if response in ['1']:
    db = create_new_card_set(db)

  elif response in ['2']:
    db = load_card_set() 

  elif response in ['3']:
    show_current_card_set(db)

  elif response in ['4']:
    add_to_existing_card_set(db)

  elif response in ['5']:
    quiz_yourself(db)

  elif response in ['q','Q','8']:
    sys.exit(0)

  return main_menu(db)
  
  
def create_new_card_set(db, e=None):

  clear_screen()
  headers.new_card_set_header()

  if e:
    cardset_name = clean( prompt(e) )

  else:
    cardset_name = clean( prompt('Please Enter a NAME for your new Flashcard Set:\n\n') )

  if db_exists(cardset_name): # file_exists default dir is db/
    e = 'This card set already exists. Please Choose Another Name:\n'
    return create_new_card_set(db, e)

  else:
    db.cur.close() #wrap up before rebinding to new db object
    db.con.close()

    db = Database(cardset_name)
    response = prompt('\nCard Set "%s" created successfully.\n\nAdd cards now? [y/N]: ' % (cardset_name))

    if response in ['y','Y']:
      response = prompt('\nDo you want to add the cards\n\n(1) manually, or \n(2) or parse them from a structured file? ')

      if response in ['1']:
        load_cards_manually(db)

      elif response in ['2']:
        load_cards_from_file(db)

    else:
      error_msg = "ERROR: You didn't provide a valid name."
      create_new_card_set(error_msg)

  return db

# ACTIVATE CARD SET
def load_card_set(error_msg=None):
  # should return a new database

  clear_screen()
  cardsets = [ (DB_DIR + f) for f in os.listdir(DB_PATH) if f.endswith('.db') ]
  cardsets.sort(key=os.path.getctime)

  if cardsets:
    prompt('Please Choose a Cardset:', False)
    print '\n'.join('({}) {}'.format(n,os.path.basename(v)) for n,v in enumerate(cardsets,start=1))  
    response = prompt() 
    if not response:
      load_card_set('Please enter a valid number in the range of %d and %d' % (1,len(cardsets)))
    response_index = int(response) - 1
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

    db.addCard(front,back)

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
    

def show_current_card_set(db):
  clear_screen()
  headers.current_card_set_header()
  prompt("Card Set: %s" % db.db_name.upper(),False)
  print_cardset(db)
  prompt('\nHit Any Key to Return to the Main Menu')

def add_to_existing_card_set(db):

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

    db.addCard(front,back)

def quiz_yourself(db,e=None):
  clear_screen()
  headers.quiz_header()
  if e:
    prompt(e,False)

  cards = load_cards_into_memory(db)
  quiz = QuizEngine(cards,db.db_name)
  
  choices = ['Randomize Cards', 'Reverse Cards', 'Keep Current Card Order']
  quiz_type = prompt( '\n'.join("({}) {}".format(num,val) for num, val in enumerate(choices, start=1)) )

  if quiz_type in ['1','2','3']:
    quiz.startQuiz(quiz_type)

  elif quiz_type in ['q','Q']:
    sys.exit(0)

  else:
    e = "That's Not a Valid Choice. (If you want to quit, enter 'q' or 'Q')"  
    return quiz_yourself(db,e)

def main(db):
  while True:
      db = main_menu(db) 

if __name__ == '__main__':
  clear_screen()
  headers.title_page()
  prompt()
  db = Database() # flashcard is default db  
  main(db)
