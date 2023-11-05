from typing import Dict, Any, List
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import Category


class CategoryRepository:
    
    def __init__(self, sess:Session):
        self.sess:Session = sess
    
    def insert_category(self, category: Category) -> bool: 
        try:
            object_mapper = Category(**category)
            self.sess.add(object_mapper)
            self.sess.commit()
        except: 
            return False 
        return True
    
    def update_category(self, id:int, details:Dict[str, Any]) -> bool: 
       try:
             self.sess.query(Category).filter(Category.id == id).update(details)     
             self.sess.commit() 
           
       except: 
           return False 
       return True
   
    def delete_category(self, id:int) -> bool: 
        try:
           category = self.sess.query(Category).filter(Category.id == id).delete()
           self.sess.commit()
          
        except: 
            return False 
        return True
    
    def get_all_category(self) -> List[Category]:
        return self.sess.query(Category).all() 
    
    def get_category(self, id:int) -> Category: 
        return self.sess.query(Category).filter(Category.id == id).one_or_none()