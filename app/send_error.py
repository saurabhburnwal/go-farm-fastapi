from fastapi.responses import JSONResponse

def send_error(message):
    return JSONResponse(
    status_code=500,
    content={"message": message},
)