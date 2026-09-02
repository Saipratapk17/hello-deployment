from fastapi import FastAPI

app = FastAPI(
    title="Hello Deployment API",
    version="2.0.0",
)


@app.get("/")
def hello_world():
    return {
        "message": "Hello World - updated",
        "version": "v2",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }