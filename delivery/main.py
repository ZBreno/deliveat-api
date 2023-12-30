from fastapi import FastAPI, Depends
from api import user, ticket, address, category, order, product, rating, product_bonus, login

app = FastAPI()
app.include_router(ticket.router)
app.include_router(rating.router)
app.include_router(address.router)
app.include_router(category.router)
app.include_router(order.router)
app.include_router(product.router)
app.include_router(user.router)
app.include_router(product_bonus.router)
app.include_router(login.router)

