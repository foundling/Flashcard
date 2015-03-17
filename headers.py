from colorama import init, Fore, Back, Style
init()

WIDTH=80
HEIGHT=24

def main_header():
  color_print('RED','H_FULL')
  color_print('RED','H_OUTER')
  color_print('RED','H_OUTER_CENTER_WORD',text='Flashcard')
  color_print('RED','H_OUTER')
  color_print('RED','H_OUTER_CENTER_WORD',text='Your Personal Quiz Engine')
  color_print('RED','H_OUTER')
  color_print('RED','H_FULL','Flashcard')

def new_card_set_header():
  print '************************************************'
  print '*                                              *'
  print '*                NEW CARD SET                  *'
  print '*                                              *'
  print '************************************************'
  print ''

def current_card_set_header():
  print '************************************************'
  print '*                                              *'
  print '*              CURRENT CARD SET                *'
  print '*                                              *'
  print '************************************************'
  print ''

def error_header(error_text):
  print '************************************************'
  print '*                                              *'
  print '*                    ERROR                     *'
  print '*                                              *'
  print '************************************************'

def load_cards_header():
  print '************************************************'
  print '*                                              *'
  print '*              LOAD CARDS MANUALLY             *'
  print '*                                              *'
  print '************************************************'
  print ''

def quiz_header():
  print '************************************************'
  print '*                                              *'
  print '*                    QUIZ !                    *'
  print '*                                              *'
  print '************************************************'

def load_cards_header():
  print '************************************************'
  print '*                                              *'

def title_page_header():
  color_print('RED','H_FULL')
  color_print('RED','H_OUTER_CENTER_WORD','Flashcard')
  color_print('RED','H_OUTER_ONLY')

def color_print(color,line_type, text=None, fill_char='*'):
  
  if color == 'RED':
    color = Fore.RED

  elif color == 'BLUE':
    color = Fore.BLUE

  if line_type == 'H_FULL':
    print color + WIDTH*'*'

  if line_type == 'H_OUTER':
    print color + \
    '*' + \
    ( (WIDTH - 2) *' ') + \
    '*'    

  if text and line_type == 'H_OUTER_CENTER_WORD':
    text = text.strip()
    text_length = len(text)
            
    total_padding = (WIDTH - (2 + len(text)) )
    if text_length%2 == 0:
      padding_before, padding_after = total_padding/2, total_padding/2
    else:
      padding_before = total_padding/2
      padding_after = total_padding/2 + 1
   
    print color + \
    '*' + \
    padding_before*' ' + \
    text + \
    padding_after*' ' + \
    '*'  
  
