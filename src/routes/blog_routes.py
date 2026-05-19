from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.models.blog_models import BlogSchema, BlogOutSchema, BlogCategory
from src.configs.db import get_db
from src.controllers import blog_controllers
from typing import List, Optional

router = APIRouter(prefix='/api/v1/blog', tags=['Blog'])

@router.get('/', response_model=List[BlogOutSchema], status_code=status.HTTP_200_OK)
def get_all_blogs(db:Session=Depends(get_db), category:Optional[BlogCategory]=None, search:Optional[str]=None):
    return blog_controllers.get_all_blogs(db, category, search)

@router.get('/{id}', response_model=BlogOutSchema, status_code=status.HTTP_200_OK)
def get_blog(id:int, db:Session=Depends(get_db)):
    return blog_controllers.get_blog(id, db)

@router.post('/create', response_model=BlogOutSchema, status_code=status.HTTP_201_CREATED)
def create_blog(request:BlogSchema, db:Session=Depends(get_db)):
    return blog_controllers.create_blog(request, db)

@router.put('/update/{id}', response_model=BlogOutSchema, status_code=status.HTTP_200_OK)
def update_blog(id:int, request:BlogSchema, db:Session=Depends(get_db)):
    return blog_controllers.update_blog(id, request, db)

@router.delete('/delete/{id}', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int, db:Session=Depends(get_db)):
    return blog_controllers.delete_blog(id, db)