from typing import Dict, Any, List
from sqlalchemy.orm import Session
from domain.data.sqlalchemy_models import Ticket
from uuid import UUID
from sqlalchemy import desc

class TicketRepository:

    def __init__(self, sess: Session):
        self.sess: Session = sess

    def insert_ticket(self, ticket: Ticket) -> bool:
        try:
            object_mapper = Ticket(**ticket)
            self.sess.add(object_mapper)
            self.sess.commit()
        except:
            return False
        return True

    def update_ticket(self, id: UUID, details: Dict[str, Any]) -> bool:
        try:
            self.sess.query(Ticket).filter(Ticket.id == id).update(details)
            self.sess.commit()

        except:
            return False
        return True

    def delete_ticket(self, id: UUID) -> bool:
        try:
            ticket = self.sess.query(Ticket).filter(Ticket.id == id).delete()
            self.sess.commit()

        except:
            return False
        return True

    def get_all_ticket(self) -> List[Ticket]:
        return self.sess.query(Ticket).all()

    def get_ticket(self, id: UUID) -> Ticket:
        return self.sess.query(Ticket).filter(Ticket.id == id).one_or_none()

    def get_last_tickets(self):
        return self.sess.query(Ticket).order_by(desc(Ticket.created_at)).limit(2).all()
