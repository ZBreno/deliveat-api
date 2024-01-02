from typing import Dict, Any, List
from sqlalchemy.orm import Session, joinedload
from domain.data.sqlalchemy_models import Product, Category, AssociationProductCategory, ProductBonus, AssociationProductBonus
from uuid import UUID, uuid4
from sqlalchemy.exc import IntegrityError


class ProductRepository:

    def __init__(self, sess: Session):
        self.sess: Session = sess

    def insert_product(self, product: Product) -> bool:
        try:
            new_product = Product(
                id=product["id"],
                name=product["name"],
                description=product["description"],
                cost=product["cost"],
                image=product["file_location"],
                user_id=product["user_id"]
            )

            if "categories" in product:
                for category_id in product["categories"]:

                    existing_category = self.sess.query(
                        Category).filter_by(id=category_id).first()

                    if existing_category:
                        association = AssociationProductCategory(
                            id=uuid4(),
                            category=existing_category)

                        new_product.categories.append(association)

                    else:
                        return False

            if "products_bonus" in product:

                for product_bonus_id in product["products_bonus"]:

                    existing_product_bonus = self.sess.query(
                        ProductBonus).filter_by(id=product_bonus_id).first()

                    if existing_product_bonus:
                        association = AssociationProductBonus(
                            id=uuid4(),
                            product_bonus=existing_product_bonus
                        )
                        new_product.products_bonus.append(association)

                    else:
                        return False

            self.sess.add(new_product)
            self.sess.commit()
        except:
            return False
        return True

    def update_product(self, id: UUID, details: Dict[str, Any]) -> bool:
        try:
            self.sess.query(Product).filter(Product.id == id).update(details)
            self.sess.commit()
        except:
            return False
        return True

    def delete_product(self, id: UUID) -> bool:
        try:
            product = self.sess.query(Product).filter(
                Product.id == id).delete()
            self.sess.commit()

        except:
            return False
        return True

    def get_all_product(self, category: str | None) -> List[Product]:
        products_query = (
            self.sess.query(Product)
            .options(
                joinedload(Product.categories)
                .joinedload(AssociationProductCategory.category)
                .load_only(Category.name)
            )
        )

        if category:
            products_query = products_query.filter(Category.name == category)

        return products_query.all()

    def get_product(self, id: UUID) -> Product:
        product = self.sess.query(Product).options(
            joinedload(Product.categories)
            .joinedload(AssociationProductCategory.category)
            .load_only(Category.name)
        ).filter(Product.id == id).one_or_none()

        return product

    def get_my_products(self, store_id: UUID) -> List[Product]:
        products_query = (
            self.sess.query(Product)
            .options(
                joinedload(Product.categories)
                .joinedload(AssociationProductCategory.category)
                .load_only(Category.name)
            ).filter(Product.user_id == store_id)
        )

        return products_query.all()
