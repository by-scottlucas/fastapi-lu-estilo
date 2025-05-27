from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from app.database.database import Base
from app.enums.role_enum import RoleEnum

class ClientModel(Base):
    __tablename__ = "tb_clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), index=True, nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)

    role = Column(
        SqlEnum(RoleEnum, name="role_enum", native_enum=False, validate_strings=True),
        default=RoleEnum.USER.value,
        nullable=False
    )
