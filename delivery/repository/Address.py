from typing import Dict, Any, List
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import Address


class AddressRepository:
    
    def __init__(self, sess:Session):
        self.sess:Session = sess
    
    def insert_address(self, address: Address) -> bool: 
        try:
            object_mapper = Address(**address)
            self.sess.add(object_mapper)
            self.sess.commit()
        except: 
            return False 
        return True
    
    def update_address(self, id:int, details:Dict[str, Any]) -> bool: 
       try:
             self.sess.query(Address).filter(Address.id == id).update(details)     
             self.sess.commit() 
           
       except: 
           return False 
       return True
   
    def delete_address(self, id:int) -> bool: 
        try:
           address = self.sess.query(Address).filter(Address.id == id).delete()
           self.sess.commit()
          
        except: 
            return False 
        return True
    
    def get_all_address(self) -> List[Address]:
        return self.sess.query(Address).all() 
    
    def get_address(self, id:int) -> Address: 
        return self.sess.query(Address).filter(Address.id == id).one_or_none()