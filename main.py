from fastapi import FastAPI
from backend.routes.chat import router as chat_router

app = FastAPI()
app.include_router(chat_router)

@app.get("/")
def health_check():
    return {"status": "BookEasyAI backend is alive "}