from fastapi import FastAPI

from app.config import settings

app = FastAPI()

@app.get(f"{settings.APP_PREFIX}", tags=["root"])
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}