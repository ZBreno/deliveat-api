import unittest
from .factories import AddressFactory, UserFactory, TicketFactory, ProductFactory, OperationFactory, ProductBonusFactory, CategoryFactory
from .test_common import Session
from domain.data.sqlalchemy_models import Address, User, Ticket, Product, Category, ProductBonus, Operation


class TestUserModel(unittest.TestCase):
    def setUp(self):
        # Prepare a new, clean session
        self.session = Session()

    def test_create_user(self):
        user = UserFactory()

        self.session.commit()

        retrieved_user = self.session.get(User, user.id)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(user.name, retrieved_user.name)

    def test_create_product(self):
        product = ProductFactory()

        self.session.commit()

        retrieved_product = self.session.get(Product, product.id)
        self.assertIsNotNone(retrieved_product)
        self.assertEqual(product.name, retrieved_product.name)

    def test_create_category(self):
        category = CategoryFactory()

        self.session.commit()

        retrieved_category = self.session.get(Category, category.id)
        self.assertIsNotNone(retrieved_category)
        self.assertEqual(category.name, retrieved_category.name)

    def test_create_ticket(self):
        ticket = TicketFactory()

        self.session.commit()

        retrieved_ticket = self.session.get(Ticket, ticket.id)
        self.assertIsNotNone(retrieved_ticket)
        self.assertEqual(ticket.code, retrieved_ticket.code)

    def test_create_address(self):
        address = AddressFactory()

        self.session.commit()

        retrieved_address = self.session.get(Address, address.id)
        self.assertIsNotNone(retrieved_address)
        self.assertEqual(f"{address.city} - {address.district} / {address.street}",
                         f"{retrieved_address.city} - {retrieved_address.district} / {retrieved_address.street}")

    def test_create_product_bonus(self):
        product_bonus = ProductBonusFactory()

        self.session.commit()

        retrieved_product_bonus = self.session.get(
            ProductBonus, product_bonus.id)
        self.assertIsNotNone(retrieved_product_bonus)
        self.assertEqual(f"{product_bonus.name}",
                         f"{retrieved_product_bonus.name}")

    def test_create_operation(self):
        operation = OperationFactory()

        self.session.commit()

        retrieved_operation = self.session.get(
            Operation, operation.id)
        self.assertIsNotNone(retrieved_operation)
        self.assertEqual(f"{operation.id}",
                         f"{retrieved_operation.id}")

    def tearDown(self):
        self.session.rollback()

        Session.remove()
