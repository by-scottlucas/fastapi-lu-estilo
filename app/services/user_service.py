from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from passlib.context import CryptContext
from app.models.client_model import ClientModel
from app.schemas.user_schema import UserBase, UserCreate, UserUpdate
from app.utils.db_exceptions import handle_db_exceptions

class UserService:
    ACCESS_DENIED = "Access denied."
    USER_NOT_FOUND = "User not found."
    CANNOT_DELETE_SELF = "You cannot delete your own user."
    ACCESS_DENIED_UPDATE = "Access denied. You can only update your own data unless you are an administrator."
    ADMIN_ROLE_REQUIRED = "Access denied. Only administrators can update user roles."
    EMAIL_ALREADY_REGISTERED = "Email already registered."
    CPF_ALREADY_REGISTERED = "CPF already registered."
    CANNOT_DELETE_OWN_USER = "You cannot delete your own user."

    def __init__(self, client_model: ClientModel):
        self.client_model = client_model
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @handle_db_exceptions
    def list_users(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 10,
        name: Optional[str] = None,
        email: Optional[str] = None
    ) -> list[UserBase]:
        query = db.query(self.client_model)

        if name:
            query = query.filter(self.client_model.name.ilike(f"%{name}%"))
        if email:
            query = query.filter(self.client_model.email.ilike(f"%{email}%"))

        return query.offset(skip).limit(limit).all()

    @handle_db_exceptions
    def get_user_by_id(
        self,
        db: Session,
        user_id: int,
        current_user: ClientModel
    ) -> ClientModel:
        if current_user.role != 'admin' and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=self.ACESS_DENIED
            )
        
        user = db.query(self.client_model)\
                .filter(self.client_model.id == user_id)\
                .first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.USER_NOT_FOUND
            )
        
        return user
    
    @handle_db_exceptions
    def get_user_by_email(self, db: Session, email: str) -> Optional[ClientModel]:
        return db.query(self.client_model)\
                 .filter(self.client_model.email == email)\
                 .first()
    
    @handle_db_exceptions
    def get_user_by_cpf(self, db: Session, cpf: str) -> Optional[ClientModel]:
        return db.query(self.client_model)\
                 .filter(self.client_model.cpf == cpf)\
                 .first()
        
    @handle_db_exceptions
    def create_user(self, db: Session, user_data: UserCreate) -> ClientModel:
        self.check_unique_email(db, user_data.email)
        self.check_unique_cpf(db, user_data.cpf)

        hashed_password = self.hash_password(user_data.password)

        new_user = self.client_model(
            name=user_data.name,
            cpf=user_data.cpf,
            email=user_data.email,
            password=hashed_password,
            role=user_data.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @handle_db_exceptions
    def update_user(
        self,
        db: Session,
        user_id: int,
        user_data: UserUpdate,
        current_user: ClientModel
    ) -> ClientModel:
        if current_user.id != user_id and current_user.role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=self.ACCESS_DENIED_UPDATE
            )

        user = self.get_user_by_id(db, user_id, current_user)
        update_fields = user_data.model_dump(exclude_unset=True)

        if "role" in update_fields and current_user.role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=self.ADMIN_ROLE_REQUIRED
            )

        if "email" in update_fields:
            self.check_unique_email(db, update_fields["email"], exclude_user_id=user_id)
        if "cpf" in update_fields:
            self.check_unique_cpf(db, update_fields["cpf"], exclude_user_id=user_id)

        for field, value in update_fields.items():
            if field == "password" and value is not None:
                user.password = self.hash_password(value)
            elif hasattr(user, field):
                setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    @handle_db_exceptions
    def delete_user(self, db: Session, user_id: int, current_user) -> None:
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=self.CANNOT_DELETE_OWN_USER
            )
        
        user = self.get_user_by_id(db, user_id, current_user)
        
        db.delete(user)
        db.commit()


    @handle_db_exceptions
    def check_unique_email(
        self,
        db: Session,
        email: str,
        exclude_user_id: Optional[int] = None
    ):
        user = self.get_user_by_email(db, email)
        if user and (exclude_user_id is None or user.id != exclude_user_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=self.EMAIL_ALREADY_REGISTERED
            )
        
    @handle_db_exceptions
    def check_unique_cpf(
        self,
        db: Session,
        cpf: str,
        exclude_user_id: Optional[int] = None
    ):
        user = self.get_user_by_cpf(db, cpf)
        if user and (exclude_user_id is None or user.id != exclude_user_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=self.CPF_ALREADY_REGISTERED
            )

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str
    ) -> bool:
        return self.pwd_context.verify(
            plain_password, hashed_password
        )

