from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from src.models.user_models import UserSchema, UserOutSchema, LoginSchema
from src.configs.db import get_db
from src.controllers import user_controllers

router = APIRouter(prefix='/api/v1/user', tags=['User'])

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserOutSchema)
def register(request: UserSchema, db:Session=Depends(get_db)):
    return user_controllers.register(request, db)

@router.post('/login', status_code=status.HTTP_200_OK, response_model=LoginSchema)
def login(request:LoginSchema, db:Session=Depends(get_db)):
    return user_controllers.login(request, db)


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_user(id: int, db:Session=Depends(get_db)):
    return user_controllers.delete_user(id, db)
