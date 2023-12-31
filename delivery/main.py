from fastapi import FastAPI, Depends
from api import user, ticket, address, category, order, product, rating, product_bonus, login
from security.secure import get_current_user

app = FastAPI()
app.include_router(ticket.router,dependencies=[Depends(get_current_user)])
app.include_router(rating.router,dependencies=[Depends(get_current_user)])
app.include_router(address.router,dependencies=[Depends(get_current_user)])
app.include_router(category.router,dependencies=[Depends(get_current_user)])
app.include_router(order.router,dependencies=[Depends(get_current_user)])
app.include_router(product.router,dependencies=[Depends(get_current_user)])
app.include_router(user.router,dependencies=[Depends(get_current_user)])
app.include_router(product_bonus.router,dependencies=[Depends(get_current_user)])
app.include_router(login.router)

