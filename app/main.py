from fastapi import FastAPI

from .routers import user, admin, category, product, public_product, cart

app = FastAPI(
    title="E-commerce REST API",
    description="A comprehensive RESTful API for an e-commerce platform.",
    version="0.1.0"
)


app.include_router(user.router)

app.include_router(admin.router)

app.include_router(category.router)

app.include_router(product.router)

app.include_router(public_product.router)

app.include_router(cart.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API!"}