import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from repository.sqlalchemy.notification import NotificationRepository
from fastapi import Query
from domain.request.notification import NotificationReq
from uuid import UUID, uuid4
from twilio.rest import Client

router = APIRouter(prefix='/notification', tags=['notification'])

def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

TWILIO_ACCOUNT_SID = 'AC4d8334617c0169fe52f792908aa3e995'
TWILIO_AUTH_TOKEN = '34cda7a2fe4599a56457a414da2c8a72'
TWILIO_PHONE_NUMBER = 'whatsapp:+14155238886'

EMAIL_SENDER = 'ze.neto429@gmail.com'
EMAIL_PASSWORD = 'qedc foli orru qxvl'

@router.post("/add")
def add_notification(req: NotificationReq, sess: Session = Depends(sess_db)):
    repo: NotificationRepository = NotificationRepository(sess)
    notification = req.model_dump()
    notification['id'] = uuid4()

    result = repo.insert_notification(notification)

    if result:
        # Enviar mensagem via WhatsApp usando Twilio
        send_whatsapp_message(notification['text'], notification['phone'])

        # Enviar e-mail de confirmação com botão
        confirmation_url = "https://sua_url.com"  # Substitua pela URL real de confirmação
        body = f"Seu e-mail foi confirmado com sucesso! Clique no botão abaixo para confirmar:\n\n" \
               f"<a href='{confirmation_url}'><button style='padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px;'>Confirmar E-mail</button></a>"
        send_confirmation_email(notification['email'], body)

        return JSONResponse(content=jsonable_encoder(notification), status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={'message': 'create notification problem encountered'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def send_whatsapp_message(message: str, number: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        from_=TWILIO_PHONE_NUMBER,
        body=message,
        to=f'whatsapp:+55{number}'
    )

    print(f"Mensagem enviada via WhatsApp SID: {message.sid}")

def send_confirmation_email(email: str, body: str):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        subject = "Confirmação de Conta"
        sender_email = EMAIL_SENDER
        receiver_email = email

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html')) 

        server.sendmail(sender_email, receiver_email, message.as_string())

        print(f"E-mail de confirmação enviado para {email}")

@router.post("/email")
async def confirm_email(email: str = Query(..., title="Endereço de e-mail para confirmação")):
    confirmation_url = "https://google.com"
    body = f"Seu e-mail foi confirmado com sucesso! Clique no botão abaixo para confirmar:\n\n" \
           f"<a href='{confirmation_url}'><button style='padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px;'>Confirmar E-mail</button></a>"
    send_confirmation_email(email, body)
    return {"message": "E-mail enviado com sucesso"}
