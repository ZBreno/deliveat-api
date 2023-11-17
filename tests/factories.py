from domain.data.sqlalchemy_models import Address, User, Ticket
from .test_common import Session
import factory
from uuid import uuid4


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = Session
        
    id = factory.Sequence(lambda n: str(uuid4()))
    name = factory.Faker('name')
    birthdate = factory.Faker('date_of_birth')
    document = factory.Sequence(lambda n: str(uuid4()))
    phone = factory.Sequence(lambda n: str(uuid4()))
    email = factory.Sequence(lambda n: str(uuid4()))
    password = factory.Faker('password')
    whatsapp = factory.Sequence(lambda n: str(uuid4()))
    instagram = factory.Sequence(lambda n: str(uuid4()))
    role = factory.Faker('random_element', elements=['company', 'client'])
    

class AddressFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Address
        sqlalchemy_session = Session
        
    id = factory.Sequence(lambda n: str(uuid4()))
    city = factory.Faker('city')
    street = factory.Faker('street_address')
    district = factory.Faker('word')
    number = factory.Faker('building_number')
    complement = factory.Faker('secondary_address')
    reference_point = factory.Faker('sentence')
    
    
class TicketFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Ticket
        sqlalchemy_session = Session
        
    id = factory.Sequence(lambda n: str(uuid4()))
    deadline = factory.Faker('date_of_birth')
    code = factory.Sequence(lambda n: str(uuid4()))
    description = factory.Faker('sentence')
    type = factory.Faker('random_element', elements=['company', 'client'])