from fastapi import FastAPI

app = FastAPI(
    title="Hello Deployment API",
    version="1.0.0",
)


@app.get("/")
def hello_world():
    return {
        "message": "Hello World",
        "version": "v1",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }