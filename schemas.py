from pydantic import BaseModel

class TodoSchema(BaseModel):
    id:int
    task:str

    class Config:
        orm_mode=True
