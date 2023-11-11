from fastapi.testclient import TestClient
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..domain.request.Ticket import TicketReq

from ..domain.data.sqlalchemy_models import Ticket

from ..main import app

client = TestClient(app)

DB_URL = "postgresql://postgres:123@localhost:5432/deliveat"

engine = create_engine(DB_URL)
session = Session(engine)

def test_ticket_model():
    ticket = TicketReq(
        deadline = date(2004,8,25).isoformat(),
        code = "#BOADIA",
        description = "30 de desconto em compras acima de R$20",
        type = "socorro")

    assert ticket.deadline == date(2004,8,25)
    assert ticket.code == "#BOADIA"
    assert ticket.description == "30 de desconto em compras acima de R$20"
    assert ticket.type == "socorro"

def test_create_ticket():
    response = client.post("/ticket/add", json={
        "deadline": date(2004,8,25).isoformat(),
        "code": "#TARDE",
        "description": "30 de desconto em compras acima de R$20",
        "type": "socorro"
        }
    )
    assert response.status_code == 201

def test_update_ticket():
    ticket = session.query(Ticket).order_by(Ticket.id.desc()).first()
    response = client.patch(f"/ticket/update/{ticket}", json={
        "deadline": date(2004,8,25).isoformat(),
        "code": "#SOCORRO",
        "description": "50 de desconto em compras acima de R$20",
        "type": "socorro"
        }
    )
    assert response.status_code == 200

def test_get_list_ticket():
    response = client.get("/ticket/list")
    assert response.status_code == 200

def test_get_ticket():
    ticket = session.query(Ticket).order_by(Ticket.id.desc()).first()
    response = client.get(f"/ticket/get/{ticket.id}")
    assert response.status_code == 200

def test_delete_ticket():
    ticket = session.query(Ticket).order_by(Ticket.id.desc()).first()
    response = client.delete(f"/ticket/delete/{ticket.id}")
    assert response.status_code == 204

