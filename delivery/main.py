from fastapi import FastAPI, Depends
from api import ticket, rating, address, category, Order, product, User

app = FastAPI()
app.include_router(ticket.router)
app.include_router(rating.router)
app.include_router(address.router)
app.include_router(category.router)
app.include_router(Order.router)
app.include_router(product.router)
app.include_router(User.router)

