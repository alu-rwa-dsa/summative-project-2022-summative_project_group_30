import uvicorn
from Backend.api import app


def run_api():
    print('Ta')
    uvicorn.run(app, port=8000)
    print("server started...")

