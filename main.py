from fastapi import FastAPI
from controllers.univap_controller import router as univap_router

app = FastAPI()
app.include_router(univap_router)