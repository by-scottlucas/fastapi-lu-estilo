from fastapi import FastAPI
from app.routes import user_routes
from app.database.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
