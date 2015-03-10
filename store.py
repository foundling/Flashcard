class Database(object):
  def __init__(self,db_name):
    open(db_name,'a+')
    self.db_name = db_name

  def add_card_to_set(self, card):
    with open(self.db_name,"a+") as _db:
      _db.write("#".join(card) + '\n')
      
