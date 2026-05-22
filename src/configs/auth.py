from fastapi import HTTPException, status, Request, Depends
from sqlalchemy.orm import Session
from src.models.user_models import UserModel
from src.configs.db import get_db
import logging
import os
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
EXP_TIME = os.getenv('EXP_TIME')

logger = logging.getLogger(__name__)

def is_authenticated(request:Request, db:Session=Depends(get_db)):
    try:
        auth_header = request.headers.get('authorization')
        token = auth_header.split(' ')[-1]

        data = jwt.decode(token, SECRET_KEY, ALGORITHM)
        print(data)
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