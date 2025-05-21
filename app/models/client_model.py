from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Client(Base):
    __tablename__ = "tb_clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
