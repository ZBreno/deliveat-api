from typing import Dict, Any, List
from sqlalchemy.orm import Session, joinedload
from domain.data.sqlalchemy_models import Order, Product, AssociationProductOrder
from uuid import UUID, uuid4


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
                user_id=order['user_id']
            )

            if "products" in order:
                for product_data in order["products"]:

                    product_id = product_data["id"]

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
                .load_only(Product.name),

            )
            .all()
        )

        # Ajuste para retornar apenas o atributo "category"
        result = [
            {
                "observation": order.observation,
                "id": order.id,
                "total": order.total,
                "code": order.code,
                "store_id": order.store_id,
                "user_id": order.user_id,
                "payment_method": order.payment_method,
                "products": [
                    {
                        "id": product.product.id,
                        "name": product.product.name,
                        "cost": product.product.cost,
                        "description": product.product.description,
                        "product_bonus": [
                            {
                                "id": product_bonus.product_bonus.id,
                                "name": product_bonus.product_bonus.name,
                                "cost": product_bonus.product_bonus.cost,
                                "description": product_bonus.product_bonus.description
                            }
                            for product_bonus in product.product.products_bonus
                        ],
                        "categories": [{"id": category.category.id, "name": category.category.name} for category in product.product.categories],
                        
                    }
                    for product in order.products
                ]
            }
            for order in orders
        ]

        return result

    def get_order(self, id: UUID) -> Order:
        return self.sess.query(Order).filter(Order.id == id).one_or_none()
