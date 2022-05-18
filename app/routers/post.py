from typing import List
from click import get_current_context
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# response_model tells us the schema for responses


@router.get("/", response_model=List[schemas.PostResponse])
# def get_posts():
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()

    print(posts)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# Adding the 'Depends' for oauth2.get_current_user ensures user is logged in to create a post
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), cur_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(
        title=post.title, content=post.content, published=post.published)
    # new_post = models.Post(**post.dict())
    db.add(new_post)  # add new post to db
    db.commit()  # commit changes
    # retrieve new post we just created and store it in new_post. Equivalent of doing RETURNING in sql
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    # print(post)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                cur_user: models.User = Depends(oauth2.get_current_user)
                ):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id, ))
    # post = cursor.fetchone()
    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} could not be deleted")
    # conn.commit()
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
cur_user: models.User = Depends(oauth2.get_current_user)):
    # sql_cmd = "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *"
    # cursor.execute(sql_cmd, (post.title, post.content, post.published, id))
    # post = cursor.fetchone()
    query = db.query(models.Post).filter(models.Post.id == id)

    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} could not be updated")
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    # conn.commit()
    return query.first()
