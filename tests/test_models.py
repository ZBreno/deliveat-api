import unittest
from .factories import AddressFactory, UserFactory, TicketFactory
from .test_common import Session
from domain.data.sqlalchemy_models import Address, User, Ticket

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
        
    def test_create_ticket(self):
        ticket = TicketFactory()

        self.session.commit()

        retrieved_ticket = self.session.get(Ticket, ticket.id)
        print(retrieved_ticket)
        self.assertIsNotNone(retrieved_ticket)
        self.assertEqual(ticket.code, retrieved_ticket.code)
        
    # def test_create_address(self):
    #     address = AddressFactory()

    #     self.session.commit()

    #     retrieved_address = self.session.get(Address, address.id)
    #     self.assertIsNotNone(retrieved_address)
    #     self.assertEqual(f"{address.city} - {address.district} / {address.street}",f"{retrieved_address.city} - {retrieved_address.district} / {retrieved_address.street}")

    def tearDown(self):
        self.session.rollback()

        Session.remove()
    