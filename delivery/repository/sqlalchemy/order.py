from typing import Dict, Any, List, Union
from sqlalchemy.orm import Session, joinedload, load_only
from domain.data.sqlalchemy_models import Order, Product, Rating, AssociationProductOrder, AssociationProductBonus, AssociationProductCategory, Address
from uuid import UUID, uuid4
from domain.response.order import OrderResponse
from datetime import datetime, timedelta
from sqlalchemy.orm import aliased
from sqlalchemy import func, select
import locale


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
                status=order['status'],
                created_at=order["created_at"],
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
            order = self.sess.query(Order).filter(Order.id == id).one_or_none()
            rating = self.sess.query(Rating).filter(
                Rating.order_id == order.id).delete()
            associantionsProduct = self.sess.query(AssociationProductOrder).filter(
                AssociationProductOrder.order_id == order.id).delete()
            order = self.sess.query(Order).filter(Order.id == id).delete()
            self.sess.commit()
        except:
            return False
        return True

    def get_all_order(self, status: str | None, code: str | None, user_id: UUID) -> List[Order]:
        orders_query = (
            self.sess.query(Order)
            .options(
                joinedload(Order.products)
                .joinedload(AssociationProductOrder.product)
                .joinedload(Product.categories)
                .joinedload(AssociationProductCategory.category),
                joinedload(Order.products)
                .joinedload(AssociationProductOrder.product)
                .joinedload(Product.products_bonus).
                joinedload(AssociationProductBonus.product_bonus)
            )
            .filter(Order.store_id == user_id)
        )

        if status:
            orders_query = orders_query.filter(Order.status == status)

        if code:
            orders_query = orders_query.filter(Order.code == code)

        result = orders_query.all()

        return result

    def get_order(self, id: UUID) -> Order:
        return self.sess.query(Order).filter(Order.id == id).one_or_none()

    def get_amount(self, user_id: UUID) -> List[Dict[str, Union[str, float]]]:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        all_days = [yesterday + timedelta(days=i)
                    for i in range((today - yesterday).days + 1)]

        orders = (
            self.sess.query(func.date_trunc('day', Order.created_at).label('day'),
                            func.sum(Order.total).label('total'))
            .filter(Order.store_id == user_id, Order.created_at >= yesterday, Order.created_at < today)
            .group_by('day')
            .all()
        )

        day_totals = {order.day.date(): order.total for order in orders}

        result = [{'date': day.strftime('%d-%m-%Y'),
                   'day': day.strftime('%A').encode('latin-1').decode('utf-8'),
                   'total': day_totals.get(day, 0)} for day in all_days]

        locale.setlocale(locale.LC_TIME, '')

        return result

    def get_amount_last_week(self, user_id: UUID):
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

        today = datetime.now().date()
        yesterday = datetime.now().date() - timedelta(days=1)

        last_week_start = today - timedelta(days=6)

        all_days = [last_week_start + timedelta(days=i) for i in range(7)]

        last_week_orders = (
            self.sess.query(func.date_trunc('day', Order.created_at).label('day'),
                            func.count(Order.id).label('total_orders'))  # Modify the query to count orders
            .filter(Order.store_id == user_id, Order.created_at >= last_week_start)
            .group_by('day')
            .all()
        )

        day_totals = {
            order.day.date(): order.total_orders for order in last_week_orders
        }

        result_last_week = [
            {
                'date': day.strftime('%d-%m-%Y'),
                'day': day.strftime('%A').encode('latin-1').decode('utf-8'),
                'total_orders': day_totals.get(day, 0)
            } for day in all_days
        ]

        locale.setlocale(locale.LC_TIME, '')

        return result_last_week

    def get_count_orders(self, user_id: UUID) -> List[Dict[str, Union[str, float]]]:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        today_orders = self.sess.query(Order).filter(
            Order.store_id == user_id, Order.created_at >= today).count()
        yesterday_orders = self.sess.query(Order).filter(
            Order.store_id == user_id, Order.created_at >= yesterday, Order.created_at < today).count()

        result_today = [{'date': today.strftime(
            '%d-%m-%Y'), 'day': today.strftime('%A'), 'total': today_orders}]
        result_yesterday = [{'date': yesterday.strftime(
            '%d-%m-%Y'), 'day': yesterday.strftime('%A'), 'total': yesterday_orders}]

        locale.setlocale(locale.LC_TIME, '')

        return result_yesterday + result_today

    def get_total_rating(self, user_id):
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

    def get_my_orders(self, user_id):
        return self.sess.query(Order).filter(Order.user_id == user_id).all()
