import random
from helper_funcs import * 

class QuizEngine(object):
  '''
  All cardset used in the quiz are copies.  The self.cards list set in init is never modified in-place. 
  we reverse cards to use the pop method.  cardset sequence relative to the end.
  '''
  
  def __init__(self,cards,cardset_name):
    self.original_cards = cards
    self.cards = None
    cards.reverse() # so we can pop from end
    self.cardset_name = cardset_name

  def init_cardset(self):
    self.cards = self.original_cards[:] # separate copy

  def shuffle_deck(self):
    random.shuffle(self.cards)

  def reverse_deck(self):
    self.cards.reverse()

  def startQuiz(self, quiz_type):
    self.init_cardset()
 
    if quiz_type in ['1']:
      self.shuffle_deck()

    if quiz_type in ['2']:
      self.reverse_deck()
    
    # SIMPLE QUIZ LOOP
    while len(self.cards):
      clear_screen()
      front, back = self.cards.pop()[:]
      prompt(front)
      prompt(back) 

    clear_screen()

    # CHANCE TO PLAY AGAIN
    response = prompt('Go Again? [y/N]')

    if response in ['y','Y']:
      choices = ['Randomize Cards', 'Reverse Cards', 'Keep Current Card Order']
      quiz_type = prompt( '\n'.join("({}) {}".format(num,val) for num, val in enumerate(choices, start=1)) )

      while quiz_type not in ['1','2','3','q','Q']:
        clear_screen()
        prompt('That\'s not a valid response. Please enter a choice from teh menu or [q/Q] to quit') 

        if quiz_type in ['1','2','3']:
          return self.startQuiz(quiz_type)

        elif quiz_type in ['q','Q']:
          sys.exit(0)

        elif quiz_type in ['m','M']: 
          return

      self.startQuiz(quiz_type)
