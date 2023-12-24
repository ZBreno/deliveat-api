from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from domain.request.ticket import TicketReq
from repository.sqlalchemy.ticket import TicketRepository
from uuid import UUID, uuid4

router = APIRouter(prefix='/ticket', tags=['Ticket'])


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_ticket(req: TicketReq, sess: Session = Depends(sess_db)):
    repo: TicketRepository = TicketRepository(sess)
    ticket = req.model_dump()
    ticket['id'] = uuid4()
    
    result = repo.insert_ticket(ticket)
    
    if result:
        return JSONResponse(content=jsonable_encoder(ticket), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create ticket problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/update/{id}")
def update_ticket(id: UUID, req: TicketReq, sess: Session = Depends(sess_db)):
    
    ticket = req.model_dump(exclude_unset=True)
    repo: TicketRepository = TicketRepository(sess)
    
    result = repo.update_ticket(id, ticket)
    
    if result:
        return JSONResponse(content=jsonable_encoder(ticket), status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message': 'update ticket error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{id}")
def delete_ticket(id: UUID, sess: Session = Depends(sess_db)):
    repo: TicketRepository = TicketRepository(sess)
    result = repo.delete_ticket(id)
    
    if result:
        return JSONResponse(content={'message': 'ticket deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content={'message': 'delete ticket error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/list")
def list_ticket(sess: Session = Depends(sess_db)):
    repo: TicketRepository = TicketRepository(sess)
    result = repo.get_all_ticket()
    return result


@router.get("/get/{id}")
def get_ticket(id: UUID, sess: Session = Depends(sess_db)):
    repo: TicketRepository = TicketRepository(sess)
    result = repo.get_ticket(id)
    return result