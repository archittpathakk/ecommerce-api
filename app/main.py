from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from app.schemas.error import APIError
from .routers import (
    user,
    admin,
    category,
    product,
    public_product,
    cart,
    order,
    admin_order,
    review,
)

app = FastAPI(
    title="E-commerce REST API",
    description="A comprehensive RESTful API for an e-commerce platform.",
    version="0.1.0"
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},  # ✅ REQUIRED BY TESTS
    )


app.include_router(user.router)
app.include_router(admin.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(public_product.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(admin_order.router)
app.include_router(review.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API!"}
