# This main.py file is our root folder where we create our fastapi application
from fastapi import FastAPI
from models import Base
from CosmeticsBE.database import engine
from routers import auth, products, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

# health check route
@app.get("/healthy")
def healthcheck():
    return {'status':'Healthy'}

app.include_router(auth.router)
# app.include_router(products.router)
app.include_router(users.router)
