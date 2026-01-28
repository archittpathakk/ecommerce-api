from fastapi import FastAPI
app = FastAPI(
    title="E-commerce REST API",
    description="A comprehensive RESTful API for an e-commerce platform.",
    version="0.1.0"
)

@app.get("/")
def read_root():

    return {"message": "Welcome to the E-commerce API!"}