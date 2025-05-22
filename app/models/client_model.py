from sqlalchemy import Column, Integer, String
from app.database.database import Base

class ClientModel(Base):
    __tablename__ = "tb_clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)