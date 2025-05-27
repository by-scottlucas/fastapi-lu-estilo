from fastapi import FastAPI
from app.routes import auth_routes, order_routes, product_routes, user_routes
from app.database.database import Base, engine

app = FastAPI(
    title="FastAPI - Lu Estilo",
    description="""
    API providing functionalities for user authentication, product management,
    order processing, and user administration. Designed to streamline
    sales operations and improve management efficiency.
    """,
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(order_routes.router)