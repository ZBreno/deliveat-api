from typing import Dict, Any, List
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import Product


class ProductRepository:
    
    def __init__(self, sess:Session):
        self.sess:Session = sess
    
    def insert_product(self, product: Product) -> bool: 
        try:
            object_mapper = Product(**product)
            self.sess.add(object_mapper)
            self.sess.commit()
        except: 
            return False 
        return True
    
    def update_product(self, id:int, details:Dict[str, Any]) -> bool: 
       try:
             self.sess.query(Product).filter(Product.id == id).update(details)     
             self.sess.commit() 
           
       except: 
           return False 
       return True
   
    def delete_product(self, id:int) -> bool: 
        try:
           product = self.sess.query(Product).filter(Product.id == id).delete()
           self.sess.commit()
          
        except: 
            return False 
        return True
    
    def get_all_product(self) -> List[Product]:
        return self.sess.query(Product).all() 
    
    def get_product(self, id:int) -> Product: 
        return self.sess.query(Product).filter(Product.id == id).one_or_none()