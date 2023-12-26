from typing import Dict, Any, List
from sqlalchemy.orm import Session, joinedload, load_only
from domain.data.sqlalchemy_models import Order, Product, AssociationProductOrder, AssociationProductCategory, AssociationProductBonus
from uuid import UUID, uuid4
from domain.response.order import OrderResponse


class OrderRepository:

    def __init__(self, sess: Session):
        self.sess: Session = sess

    def insert_order(self, order: Order) -> bool:
        try:
            new_order = Order(
                id=order["id"],
                total=order["total"],
                observation=order["observation"],
                address_id=order["address_id"],
                store_id=order["store_id"],
                code=order["code"],
                payment_method=order["payment_method"],
                user_id=order['user_id'],
                status=order['status']
            )

            if "products" in order:
                for product_id in order["products"]:

                    existing_product = self.sess.query(
                        Product).filter_by(id=product_id).first()

                    if existing_product:
                        association = AssociationProductOrder(
                            id=uuid4(),
                            product=existing_product)

                        new_order.products.append(association)

                    else:
                        return False

            self.sess.add(new_order)
            self.sess.commit()
        except:
            return False
        return True

    def update_order(self, id: UUID, details: Dict[str, Any]) -> bool:
        try:
            self.sess.query(Order).filter(Order.id == id).update(details)
            self.sess.commit()
        except:
            return False
        return True

    def delete_order(self, id: UUID) -> bool:
        try:
            order = self.sess.query(Order).filter(Order.id == id).delete()
            self.sess.commit()
        except:
            return False
        return True

    def get_all_order(self) -> List[Order]:
        orders = (
            self.sess.query(Order)
            .options(
                joinedload(Order.products)
                .joinedload(AssociationProductOrder.product)
                .joinedload(Product.categories)

            )
            .options(
                joinedload(Order.products)
                .joinedload(AssociationProductOrder.product)
                .joinedload(Product.products_bonus)
            )
            .all()


        )

        return orders

    def get_order(self, id: UUID) -> Order:
        return self.sess.query(Order).filter(Order.id == id).one_or_none()
