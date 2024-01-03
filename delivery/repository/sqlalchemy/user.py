from typing import Dict, Any, List
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import User, Address
from uuid import UUID
from domain.data.enums.role import RoleChoice


class UserRepository:

    def __init__(self, sess: Session):
        self.sess: Session = sess

    def insert_user(self, user: User) -> bool:
        try:
            object_mapper = User(**user)
            self.sess.add(object_mapper)
            self.sess.commit()
        except:
            return False
        return True

    def update_user(self, id: UUID, details: Dict[str, Any]) -> bool:
        try:
            self.sess.query(User).filter(User.id == id).update(details)
            self.sess.commit()

        except:
            return False
        return True

    def delete_user(self, id: UUID) -> bool:
        try:
            user = self.sess.query(User).filter(User.id == id).delete()
            self.sess.commit()

        except:
            return False
        return True

    def get_all_user(self) -> List[User]:
        return self.sess.query(User).all()

    def get_user(self, id: UUID) -> User:
        return self.sess.query(User).filter(User.id == id).one_or_none()

    def get_user_me(self, email: str) -> User:
        return self.sess.query(User).filter(User.email == email).one_or_none()

    def get_stories(self) -> List[User]:
        return self.sess.query(User).filter(User.role == RoleChoice.STORE).all()
    
    def get_addresses(self) -> List[Address]:
        return [address.address for address in self.addresses]
    
    def get_establishment(self):
        results = self.sess.query(User.name, User.profile_picture, User.id).filter(
            User.role == RoleChoice.STORE).all()

        establishment_data = [{"name": name, "profile_picture": profile_picture, "id": id}
                              for name, profile_picture, id in results]

        return establishment_data
