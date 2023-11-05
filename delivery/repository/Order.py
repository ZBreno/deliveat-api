from typing import Dict, Any, List
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import Order


class OrderRepository:
    
    def __init__(self, sess:Session):
        self.sess:Session = sess
    
    def insert_order(self, order: Order) -> bool: 
        try:
            object_mapper = Order(**order)
            self.sess.add(object_mapper)
            self.sess.commit()
        except: 
            return False 
        return True
    
    def update_order(self, id:int, details:Dict[str, Any]) -> bool: 
       try:
             self.sess.query(Order).filter(Order.id == id).update(details)     
             self.sess.commit() 
           
       except: 
           return False 
       return True
   
    def delete_order(self, id:int) -> bool: 
        try:
           order = self.sess.query(Order).filter(Order.id == id).delete()
           self.sess.commit()
          
        except: 
            return False 
        return True
    
    def get_all_order(self) -> List[Order]:
        return self.sess.query(Order).all() 
    
    def get_order(self, id:int) -> Order: 
        return self.sess.query(Order).filter(Order.id == id).one_or_none()