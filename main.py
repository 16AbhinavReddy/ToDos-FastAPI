from fastapi import FastAPI
import models
from database import engine
from Routers import auth, todos

app = FastAPI()

models.base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.Router)