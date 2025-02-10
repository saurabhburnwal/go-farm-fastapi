
from fastapi import FastAPI, HTTPException
from app.database import database
from app.models import  users, results
from app.schemas import  UserAuth, UserSignup
from app.generate_random import generate_random



async def get_user(user:UserAuth):
    query = users.select().where(users.c.username == user.username, users.c.password == user.password)
    return await database.fetch_one(query)

async def get_user_from_token(token:str):
    query = users.select().where(users.c.token == token)
    return await database.fetch_one(query)

async def create_user(user: UserSignup):
    query = users.select().where(users.c.username == user.username, users.c.password == user.password)
    existingUser =  await database.fetch_one(query)
    if existingUser is not None :
         raise HTTPException(status_code=404, detail="User already exists")
    else:
        query = users.insert().values(username=user.username, password=user.password, token=generate_random(), email= user.email, name=user.name )
        last_record_id = await database.execute(query)
        return {"data":True}

async def save_result(author:str, content:str):
    query = results.insert().values(author=author, content=content)
    last_record_id = await database.execute(query)
    return last_record_id

async def get_results(username: str):
    query = results.select().where(results.c.author == username)
    return await database.fetch_all(query)