from fastapi import FastAPI
from app.routing.main_router import main_router


app = FastAPI()


app.include_router(main_router)
