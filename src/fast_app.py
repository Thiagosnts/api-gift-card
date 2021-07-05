#! /usr/bin/python python3
from fastapi import FastAPI,Request
import uuid
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.exceptions import RequestValidationError
from src.rest.errors import build_error_response


from src.rest.routes import router


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request.state.debug_id = str(uuid.uuid4())
    response = await call_next(request)
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return build_error_response(request, exc)


@app.exception_handler(Exception)
async def all_exceptions(request, exc):
    return build_error_response(request, exc)


app.include_router(router)




if __name__ == '__main__':
    uvicorn.run(app,
                host='0.0.0.0',
                port='8281')
