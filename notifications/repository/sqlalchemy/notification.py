from typing import Dict, Any, List
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import Notification
from uuid import UUID


class NotificationRepository:

    def __init__(self, sess: Session):
        self.sess: Session = sess

    def insert_notification(self, notification: Notification) -> bool:
        try:
            object_mapper = Notification(**notification)
            self.sess.add(object_mapper)
            self.sess.commit()
        except:
            return False
        
        return True

    def update_notification(self, id: UUID, details: Dict[str, Any]) -> bool:
        try:
            self.sess.query(Notification).filter(Notification.id == id).update(details)
            self.sess.commit()

        except:
            return False
        return True

    def delete_notification(self, id: UUID) -> bool:
        try:
            notification = self.sess.query(Notification).filter(Notification.id == id).delete()
            self.sess.commit()

        except:
            return False
        return True

    def get_all_notification(self) -> List[Notification]:
        return self.sess.query(Notification).all()

    def get_notification(self, id: UUID) -> Notification:
        return self.sess.query(Notification).filter(Notification.id == id).one_or_none()
