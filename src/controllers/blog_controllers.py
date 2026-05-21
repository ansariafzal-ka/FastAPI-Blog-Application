from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from src.models.blog_models import BlogModel, BlogSchema, BlogCategory
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def get_all_blogs(db:Session, category:Optional[BlogCategory], search:Optional[str]):
    try:
        query = db.query(BlogModel)
        
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

def get_blog(id:int, db:Session):
    try:
        blog = db.query(BlogModel).get(id)

        if not blog:
            logger.error(f'Blog not found with id: {id}')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Blog not found'
            )
        
        return blog
    
    except Exception as e:
        logger.error(f'Failed to get the blog: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to get the blog'
        )

def create_blog(request:BlogSchema, db:Session):
    try:
        new_blog = BlogModel(
            title = request.title,
            content = request.content,
            category = request.category
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

def update_blog(id:int, request:BlogSchema, db:Session):
    try:
        blog = db.query(BlogModel).get(id)

        if not blog:
            logger.error(f'Blog not found with id: {id}')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Blog not found'
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

def delete_blog(id:int, db:Session):
    try:
        blog = db.query(BlogModel).get(id)

        if not blog:
            logger.error(f'Blog not found with id: {id}')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Blog not found'
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