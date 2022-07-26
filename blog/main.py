from ast import Delete
from fastapi import FastAPI,Depends,HTTPException,status
from .database import get_db,SessionLocal,Base,engine
from .import models
from .schemas import Blog


app = FastAPI(title="Routers in FastAPI")

#Creating all database table
models.Base.metadata.create_all(bind=engine)

@app.post('/blog',tags=['Blogs'])
def blog(request:Blog,db:SessionLocal=Depends(get_db)):
    blog_data = models.Blog(title=request.title,blog=request.blog)
    db.add(blog_data)
    db.commit()
    db.refresh(blog_data)
    return blog_data

@app.get('/blog',tags=['Blogs'])
def all_blog(db:SessionLocal=Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog

@app.get('/blog/{id}',tags=['Blogs'])
def all_blog(id,db:SessionLocal=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'Blog id {id} is Not Found!')
    return blog

@app.delete('/blog/{id}',tags=['Blogs'])
def delete_blog(id,db:SessionLocal=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'Blog id {id} is Not Found!')
    db.delete(blog)
    db.commit()
    return 'Blog is deleted'
    