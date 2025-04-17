from fastapi import FastAPI
from api import webhook_router
app = FastAPI()
app.include_router(webhook_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
