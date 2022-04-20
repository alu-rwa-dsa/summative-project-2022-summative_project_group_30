import uvicorn
from Backend.api import app
from configs.db_conn import connect_db


def run_api():
    connect_db()
    uvicorn.run(app, port=8000)




