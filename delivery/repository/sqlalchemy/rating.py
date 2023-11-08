from typing import Dict, Any, List
from sqlalchemy.orm import Session
from ...domain.data.sqlalchemy_models import Rating
from uuid import UUID


class RatingRepository:

    def __init__(self, sess: Session):
        self.sess: Session = sess

    def insert_rating(self, rating: Rating) -> bool:
        try:
            object_mapper = Rating(**rating)
            self.sess.add(object_mapper)
            self.sess.commit()
        except:
            return False
        return True

    def update_rating(self, id: UUID, details: Dict[str, Any]) -> bool:
        try:
            self.sess.query(Rating).filter(Rating.id == id).update(details)
            self.sess.commit()

        except:
            return False
        return True

    def delete_rating(self, id: UUID) -> bool:
        try:
            rating = self.sess.query(Rating).filter(Rating.id == id).delete()
            self.sess.commit()

        except:
            return False
        return True

    def get_all_rating(self) -> List[Rating]:
        return self.sess.query(Rating).all()

    def get_rating(self, id: UUID) -> Rating:
        return self.sess.query(Rating).filter(Rating.id == id).one_or_none()
