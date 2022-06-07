from http.client import HTTPException
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from database import SessionLocal, db_engine
from models import TODO,Base
from schemas import TodoSchema
from sqlalchemy.orm import sessionmaker,Session
from typing import Optional,List
from fastapi.responses import JSONResponse

api=FastAPI()
# class Task(BaseModel):
#     id:int
#     desc:str
#     is_completed:Optional[bool]
# class Todo(BaseModel):
#     id:int
#     task:str

#     class Config:
#         orm_mode:True

Base.metadata.create_all(db_engine)  
session=sessionmaker(bind=db_engine)  

# @api.get("/test")
# def index():
#     return {'data':['list']}

# @api.get('/blog/{id}')
# def show(id:int):
#     return {'data':id}    

# @api.get('/tasks')
# def getTasks(limit):
#     return {'data':f'showing {limit} tasks from your todo list '}    

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@api.post('/addnewtask',response_model=TodoSchema)
def create_new_task(newtask:TodoSchema,db:Session=Depends(get_db)):
    new_task=TODO(id=newtask.id,task=newtask.task)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
    
@api.get('/getalltasks',response_model=List[TodoSchema])
def getTasks(db:Session=Depends(get_db)):
    return db.query(TODO).all();

@api.put('/updatetask/{id}',response_model=TodoSchema)
def updateTask(task:str,id:int,db:Session=Depends(get_db)):
    try:
        res=db.query(TODO).filter(TODO.id==id).first()
        res.task=task
        db.add(res)
        db.commit()
        db.refresh(res)
        return res
    except :
        return HTTPException(status_code=400,detail="task not found with this id")

@api.delete('/deletetask/{id}',response_class=JSONResponse)  
def deleteTask(id:int,db:Session=Depends(get_db)):
    try:
        task=db.query(TODO).filter(TODO.id==id).first()
        db.delete(task)
        db.commit()
        return {f"task with id={id} has been deleted":True}
    except :
        HTTPException(status_code=404,detail="task does not exists")          

