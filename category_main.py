import uvicorn
from fastapi import FastAPI
from categories.category import category_router

app = FastAPI()

app.include_router(category_router)
uvicorn.run(app, host="localhost", port=5003)
