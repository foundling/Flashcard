from colorama import init, Fore, Back, Style
init(autoreset=True)

class ColorPrinter(object):
   pass 

WIDTH=80
HEIGHT=24

def main_header():
  color_print('RED','FULL')
  color_print('RED','OUTER')
  color_print('RED','OUTER_CENTER_TEXT',text='Flashcard')
  color_print('RED','OUTER')
  color_print('RED','OUTER_CENTER_TEXT',text='Your Personal Quiz Engine')
  color_print('RED','OUTER')
  color_print('RED','FULL','Flashcard')

def new_card_set_header():
  color_print('RED','FULL')
  color_print('RED','OUTER')
  color_print('RED','OUTER_CENTER_TEXT',text='New Card Set')
  color_print('RED','OUTER')
  color_print('RED','FULL','Flashcard')

def title_page():
  print ''
  color_print('RED','FULL', fill_char='-')
  color_print('','CENTER_TEXT',text='FLASHCARD')
  color_print('BLUE','FULL', fill_char = '-')
  color_print('','CENTER_TEXT',text='Your Personal Quiz Engine')
  color_print('BLUE','FULL', fill_char = '-')
  print ''
  color_print('BLUE','FULL', fill_char = '-')
  print ''
  color_print('BLUE','FULL', fill_char = '-')
  print ''
  color_print('BLUE','FULL', fill_char = '-')
  print ''
  color_print('BLUE','FULL', fill_char = '-')

def current_card_set_header():
  print '*              CURRENT CARD SET                *'

def error_header(error_text):
  print '*                    ERROR                     *'

def load_cards_header():
  print '*              LOAD CARDS MANUALLY             *'

def quiz_header():
  print '*                    QUIZ !                    *'

def load_cards_header():
  print '************************************************'


def color_print(color, line_type, text=None, fill_char='*'):
  FC = fill_char

  if color == 'RED':
    color = Fore.RED


  elif color == 'BLUE':
    color = Fore.BLUE

  elif color == 'BLACK':
    color = Fore.BLACK

  else:
    color = ''

  if line_type == 'FULL':
    print color + WIDTH*FC

  if line_type == 'OUTER':
    print color + \
    FC + \
    ( (WIDTH - 2) *' ') + \
    FC    

  if text and line_type == 'CENTER_TEXT':
    text = text.strip()
    text_length = len(text)
    total_padding = (WIDTH - (0 + len(text)) )

    if text_length%2 == 0:
      padding_before, padding_after = total_padding/2, total_padding/2

    else:
      padding_before = total_padding/2
      padding_after = total_padding/2 + 1

    print color + \
    padding_before*' ' + \
    text + \
    padding_after*' ' 

  if text and line_type == 'OUTER_CENTER_TEXT':
    text = text.strip()
    text_length = len(text)
    total_padding = (WIDTH - (2 + len(text)) )

    if text_length%2 == 0:
      padding_before, padding_after = total_padding/2, total_padding/2

    else:
      padding_before = total_padding/2
      padding_after = total_padding/2 + 1
   
    print color + \
    FC + \
    padding_before*' ' + \
    text + \
    padding_after*' ' + \
    FC  
