from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from models import ToDos
from sqlalchemy.orm import Session
from database import sessionlocal
from pydantic import BaseModel, Field
from .auth import get_curr_user

Router = APIRouter()

# Router.include_router(auth.router)
# models.base.metadata.create_all(bind=engine)

class Todo_Request(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=3, max_length=100)
    priority : int = Field(gt=0)
    complete : bool

def get_data() :
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_data)]
user_dependency = Annotated[dict, Depends(get_curr_user)]

@Router.get('/items/')

async def get_items(user: user_dependency, db : db_dependency):
    if user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed Authentication !!!")
    return db.query(ToDos).filter(ToDos.owner_id == user.get('user_ID')).all()

@Router.get('/todo/{todo_id}', status_code= status.HTTP_200_OK)

async def get_id(user: user_dependency, db : db_dependency, todo_id : int = Path(gt=0)):
    if user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed Authentication !!!")
    todo_list = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('user_ID')).first()
    if todo_list is not None :
        return todo_list
    raise HTTPException(status_code=404, detail='The data you have asked is not found')

@Router.post('/todo_post/', status_code=status.HTTP_201_CREATED)

async def create_todo(user : user_dependency, db : db_dependency, todo_request : Todo_Request):
    if user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed Authentication !!!")
    todo_model = ToDos(**todo_request.dict(), owner_id=user.get('user_ID'))
    db.add(todo_model)
    db.commit()

@Router.put('/todo_update/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)

async def update_todo(user : user_dependency, db : db_dependency, todo_request : Todo_Request, todo_id : int = Path(gt=0)) :
    if user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed Authentication !!!")
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('user_ID')).first()
    if todo_model is None :
        raise HTTPException(status_code=404, detail='The data you want is not found')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@Router.delete('/todo_delete/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)

async def delete_todo(user : user_dependency, db : db_dependency, todo_id : int = Path(gt=0)) :
    if user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed Authentication !!!")
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('user_ID')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='The data you want is not found')
    db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('user_ID')).delete()
    db.commit()