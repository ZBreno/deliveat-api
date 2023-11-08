from fastapi import FastAPI, Depends
from .api import ticket, rating, address, category, order, product, user

app = FastAPI()
app.include_router(ticket.router)
app.include_router(rating.router)
app.include_router(address.router)
app.include_router(category.router)
app.include_router(order.router)
app.include_router(product.router)
app.include_router(user.router)

