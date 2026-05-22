from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from src.models.blog_models import BlogModel, BlogSchema, BlogCategory
from src.models.user_models import UserModel
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def get_all_blogs(db:Session, category:Optional[BlogCategory], search:Optional[str], user:UserModel):
    try:
        query = db.query(BlogModel).filter(BlogModel.user_id == user.id)
        
        if category:
            query = query.filter(BlogModel.category == category)
        if search:
            query = query.filter(BlogModel.title.contains(search))
        
        blogs = query.all()

        return blogs
    
    except Exception as e:
        logger.error(f'Failed to get all blogs: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to get all blogs'
        )

def get_blog(id:int, db:Session, user:UserModel):
    try:
        blog = db.query(BlogModel).get(id)

        if not blog:
            logger.error(f'Blog not found with id: {id}')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Blog not found'
            )
        
        if blog.user_id != user.id:
            logger.error('You are not authorized to access this blog')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='You are not authorized to access this blog'
            )
        
        return blog
    
    except Exception as e:
        logger.error(f'Failed to get the blog: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to get the blog'
        )

def create_blog(request:BlogSchema, db:Session, user:UserModel):
    try:
        new_blog = BlogModel(
            title = request.title,
            content = request.content,
            category = request.category,
            user_id = user.id
        )

        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)

        return new_blog
    
    except Exception as e:
        logger.error(f'Failed to create the blog: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to create the blog'
        )

def update_blog(id:int, request:BlogSchema, db:Session, user:UserModel):
    try:
        blog = db.query(BlogModel).get(id)

        if not blog:
            logger.error(f'Blog not found with id: {id}')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Blog not found'
            )
        
        if blog.user_id != user.id:
            logger.error('You are not authorized to update this blog')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='You are not authorized to update this blog'
            )
        
        blog.title = request.title
        blog.content = request.content
        blog.category = request.category

        db.commit()
        db.refresh(blog)

        return blog
    
    except Exception as e:
        logger.error(f'Failed to update the blog: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to update the blog'
        )

def delete_blog(id:int, db:Session, user:UserModel):
    try:
        blog = db.query(BlogModel).get(id)

        if not blog:
            logger.error(f'Blog not found with id: {id}')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Blog not found'
            )
        
        if blog.user_id != user.id:
            logger.error('You are not authorized to delete this blog')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='You are not authorized to delete this blog'
            )
        
        db.delete(blog)
        db.commit()

        return None
    
    except Exception as e:
        logger.error(f'Failed to delete the blog: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to delete the blog'
        )