class Database(object):
 
  def __init__(self,db_name):
    try: 
      open(db_name)
    except IOError:
      print "Couldn't open this file, it doesn't exist"  
    else:
      self.db_name = db_name

