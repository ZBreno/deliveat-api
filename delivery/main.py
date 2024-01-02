from fastapi import FastAPI, Depends
from api import user, ticket, address, category, order, product, rating, product_bonus, login
from security.secure import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # Permitir qualquer método HTTP
    allow_headers=["*"],  # Permitir qualquer cabeçalho
)

app.include_router(ticket.router)
app.include_router(rating.router)
app.include_router(address.router)
app.include_router(category.router)
app.include_router(order.router)
app.include_router(product.router)
app.include_router(user.router)
app.include_router(product_bonus.router)
app.include_router(login.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

