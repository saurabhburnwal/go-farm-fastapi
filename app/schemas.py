from pydantic import BaseModel

class ResultBody(BaseModel):
    content:str

class UserAuth(BaseModel):
    username: str
    password: str

class UserSignup(UserAuth):
    email: str
    name: str

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int

    class Config:
        orm_mode = True