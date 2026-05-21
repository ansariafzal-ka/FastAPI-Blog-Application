from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from src.models.user_models import UserModel, UserSchema, LoginSchema
from pwdlib import PasswordHash
import logging
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
EXP_TIME = os.getenv('EXP_TIME')

logger = logging.getLogger(__name__)
password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def register(request:UserSchema, db:Session):
    try:
        is_user = db.query(UserModel).filter(UserModel.user_name == request.user_name).first()
        if is_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= 'Username already exist..'
            )
        
        is_user = db.query(UserModel).filter(UserModel.email == request.email).first()
        if is_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= 'Email already exist..'
            )
        
        hashed_password = get_password_hash(request.password)
        new_user = UserModel(
            user_name = request.user_name,
            email = request.email,
            hash_password = hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    except Exception as e:
        logger.error(f'Failed to register user: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to register user.'
        )
    
def login(request:LoginSchema, db:Session):
    try:
        user = db.query(UserModel).filter(UserModel.user_name == request.user_name).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Credentials...'
            )
        
        if not verify_password(request.password, user.hash_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Credentials...'
            ) 
        
        exp_time = datetime.now() + timedelta(minutes=EXP_TIME)
        
        token = jwt.encode({'_id': user.id, 'exp': exp_time}, SECRET_KEY, ALGORITHM)

        return {'token': token}

    except Exception as e:
        logger.error(f'Failed to login user: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to login user.'
        )
    
def delete_user(id:int, db:Session):
    try:
        user = db.query(UserModel).get(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        
        db.delete(user)
        db.commit()

        return None
    
    except Exception as e:
        logger.error(f'Failed to delete the user: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to delete the user'
        )