from fastapi import FastAPI, HTTPException,Request
from app.schemas import  UserAuth, ResultBody, UserSignup
from app.database import database, metadata, engine
from app.crud import  create_user, get_user, get_user_from_token, save_result, get_results
from app.calculate_result import calculate_result
from fastapi.middleware.cors import CORSMiddleware
from app.send_error import send_error
from contextlib import asynccontextmanager

metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
async def read_message(user: UserAuth):
   
    user = await get_user(user)
    if user is None:
        return send_error("Username or password is wrong")
    return {"data":user} 

@app.post("/signup")
async def create_message_endpoint(user: UserSignup):
    return await create_user(user)

@app.get("/results")
async def read_message(request:Request):
    auth_token = request.headers.get('Authorization')
    user = await get_user_from_token(auth_token)
    if user is None:
        return send_error("User not found")
    results = await get_results(user.username);
    return results

@app.get("/yields")
async def read_message(state:str,  area:str):
   rice = calculate_result(state, "RICE", area)
   wheat = calculate_result(state, "WHEAT", area)
   maze = calculate_result(state, "MAZE", area)
   barley = calculate_result(state, "BARLEY", area)
   data = {"rice":rice, "wheat":wheat, "maze":maze, "barley":barley}
   return {"data":data}

@app.get("/states-comparison")
async def read_message(state1:str, state2:str, state3:str, state4:str, area:str):
   
    #Rice
    state1Rice = calculate_result(state1, "RICE", area)
    state2Rice = calculate_result(state2, "RICE", area)
    state3Rice = calculate_result(state3, "RICE", area)
    state4Rice = calculate_result(state4, "RICE", area)

    rice = [state1Rice, state2Rice, state3Rice, state4Rice]

    #Wheat
    state1Wheat = calculate_result(state1, "WHEAT", area)
    state2Wheat = calculate_result(state2, "WHEAT", area)
    state3Wheat = calculate_result(state3, "WHEAT", area)
    state4Wheat = calculate_result(state4, "WHEAT", area)
    wheat = [state1Wheat, state2Wheat, state3Wheat, state4Wheat]

    #Maze
    state1maze = calculate_result(state1, "MAZE", area)
    state2maze = calculate_result(state2, "MAZE", area)
    state3maze = calculate_result(state3, "MAZE", area)
    state4maze = calculate_result(state4, "MAZE", area)

    maze = [state1maze, state2maze, state3maze, state4maze]

    #Barley
    state1Barley = calculate_result(state1, "BARLEY", area)
    state2Barley = calculate_result(state2, "BARLEY", area)
    state3Barley = calculate_result(state3, "BARLEY", area)
    state4Barley = calculate_result(state4, "BARLEY", area)

    barley = [state1Barley, state2Barley, state3Barley, state4Barley]


    data = {"rice":rice, "wheat":wheat, "maze":maze, "barley":barley}
    return {"data":data}

@app.post("/result")
async def create_message_endpoint(request:Request, body: ResultBody):
    auth_token = request.headers.get('Authorization')
    user = await get_user_from_token(auth_token)
    savedItem = await save_result(user.username, body.content)
    return savedItem

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


