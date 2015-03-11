def addnewlines(newline_count = 1):
  newline = ''
  nl = '\n'
  for i in range(newline_count + 1):
    newline += nl
  print newline

addnewlines(4)
