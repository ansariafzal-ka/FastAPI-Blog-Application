from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from src.models.user_models import UserSchema, UserOutSchema, LoginSchema, UserModel
from src.configs.db import get_db
from src.controllers import user_controllers
from src.configs.auth import is_authenticated

router = APIRouter(prefix='/api/v1/user', tags=['User'])

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserOutSchema)
def register(request: UserSchema, db:Session=Depends(get_db)):
    return user_controllers.register(request, db)

@router.post('/login', status_code=status.HTTP_200_OK)
def login(request:LoginSchema, db:Session=Depends(get_db)):
    return user_controllers.login(request, db)

@router.get('/auth', status_code=status.HTTP_200_OK, response_model=UserOutSchema)
def is_authenticated(request:Request, db:Session=Depends(get_db)):
    return user_controllers.is_authenticated(request, db)

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_user(id: int, db:Session=Depends(get_db), current_user:UserModel=Depends(is_authenticated)):
    return user_controllers.delete_user(id, db, current_user)
