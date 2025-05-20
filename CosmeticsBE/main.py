# This main.py file is our root folder where we create our fastapi application
from mangum import Mangum
from fastapi import FastAPI
from models import Base
from database import engine
from routers import auth, products, users, categories, cart, orders
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)


origins = [
    "http://127.0.0.1:8000",
    "*",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# handler = Mangum(app)

# health check route
@app.get("/healthy")
def healthcheck():
    return {'status':'Healthy'}

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(cart.router)
app.include_router(orders.router)
