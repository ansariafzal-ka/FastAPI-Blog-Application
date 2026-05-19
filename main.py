from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from src.configs.db import engine, Base
from src.routes.blog_routes import router as blog_router

Base.metadata.create_all(engine)

app = FastAPI(title='Blog Application')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)

app.include_router(blog_router)

@app.get('/health', status_code=status.HTTP_200_OK)
def health_check():
    return {'status': 200}