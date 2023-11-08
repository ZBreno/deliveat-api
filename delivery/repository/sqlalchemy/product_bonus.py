from typing import Dict, Any, List
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import ProductBonus
from uuid import UUID


class ProductBonusRepository:

    def __init__(self, sess: Session):
        self.sess: Session = sess

    def insert_product_bonus(self, product_bonus: ProductBonus) -> bool:
        try:
            object_mapper = ProductBonus(**product_bonus)
            self.sess.add(object_mapper)
            self.sess.commit()
        except:
            return False
        return True

    def update_product_bonus(self, id: UUID, details: Dict[str, Any]) -> bool:
        try:
            self.sess.query(ProductBonus).filter(ProductBonus.id == id).update(details)
            self.sess.commit()

        except:
            return False
        return True

    def delete_product_bonus(self, id: UUID) -> bool:
        try:
            ProductBonus = self.sess.query(ProductBonus).filter(
                ProductBonus.id == id).delete()
            self.sess.commit()

        except:
            return False
        return True

    def get_all_product_bonus(self) -> List[ProductBonus]:
        return self.sess.query(ProductBonus).all()

    def get_product_bonus(self, id: UUID) -> ProductBonus:
        return self.sess.query(ProductBonus).filter(ProductBonus.id == id).one_or_none()
