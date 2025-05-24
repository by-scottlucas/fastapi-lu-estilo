from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps

def handle_db_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {error}"
            )
    return wrapper
