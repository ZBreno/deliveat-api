from fastapi import FastAPI, Depends
from api import user, ticket, address, category, order, product, rating, product_bonus, login
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        content={"detail": exc.errors(), "body": exc.body},
        status_code=422,
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
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

