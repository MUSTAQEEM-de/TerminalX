from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="LinuXpert API",
    description="AI-powered Linux assistant",
    version="1.0.0"
)


class CommandRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "message": "LinuXpert API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/command")
def command(request: CommandRequest):
    return {
        "user_input": request.text,
        "message": "Command received successfully"
    }