from typing import Dict, Any, List
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import User
from uuid import UUID


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