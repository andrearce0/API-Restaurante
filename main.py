from database import engine, Base
from fastapi import FastAPI
from rotas import router
from rotas_auth import router_auth
import modelos

app = FastAPI()

app.include_router(router)
app.include_router(router_auth)

Base.metadata.create_all(bind=engine)