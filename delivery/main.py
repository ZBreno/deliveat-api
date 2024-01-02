from fastapi import FastAPI, Depends
from api import user, ticket, address, category, order, product, rating, product_bonus, login
from security.secure import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(ticket.router,dependencies=[Depends(get_current_user)])
app.include_router(rating.router,dependencies=[Depends(get_current_user)])
app.include_router(address.router,dependencies=[Depends(get_current_user)])
app.include_router(category.router,dependencies=[Depends(get_current_user)])
app.include_router(order.router,dependencies=[Depends(get_current_user)])
app.include_router(product.router,dependencies=[Depends(get_current_user)])
app.include_router(user.router,dependencies=[Depends(get_current_user)])
app.include_router(product_bonus.router,dependencies=[Depends(get_current_user)])
app.include_router(login.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

