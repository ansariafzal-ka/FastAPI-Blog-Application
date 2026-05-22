from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from src.models.user_models import UserModel, UserSchema, LoginSchema
from pwdlib import PasswordHash
import logging
import jwt
from jwt.exceptions import InvalidTokenError
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
        
        exp_time = datetime.now() + timedelta(minutes=int(EXP_TIME))
        token = jwt.encode({'_id': user.id, 'exp_time': exp_time.timestamp()}, SECRET_KEY, ALGORITHM)

        return {'token': token}

    except Exception as e:
        logger.error(f'Failed to login user: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to login user.'
        )
    
def is_authenticated(request:Request, db:Session):
    try:
        auth_header = request.headers.get('authorization')
        token = auth_header.split(' ')[-1]

        data = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = data.get('_id')
        exp_time = data.get('exp_time')

        current_time = datetime.now().timestamp()
        if current_time > exp_time:
            logger.error('You are unauthorized')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='You are unauthorized'
            )
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            logger.error('You are unauthorized')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='You are unauthorized'
            )

        return user
    
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='You are unauthorized.'
        )

def delete_user(id:int, db:Session, current_user:UserModel):
    try:
        user = db.query(UserModel).get(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        
        if user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You are not authorized to delete this user'
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