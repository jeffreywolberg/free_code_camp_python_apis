from typing import List, Optional
from click import get_current_context
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# response_model tells us the schema for responses


@router.get("/", response_model=List[schemas.PostWithVotesResponse])
# def get_posts():
def get_posts(db: Session = Depends(get_db),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):
    vote_count = func.count(models.Post.id)
    results = db.query(models.Post, vote_count.label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
        models.Post.id).order_by(vote_count.desc()).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # line below if only getting posts that belong to current user
    # posts = db.query(models.Post).filter(models.Post.owner_id == cur_user.id).all()
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# Adding the 'Depends' for oauth2.get_current_user ensures user is logged in to create a post
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), cur_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=cur_user.id, **post.dict())
    db.add(new_post)  # add new post to db
    db.commit()  # commit changes
    # retrieve new post we just created and store it in new_post. Equivalent of doing RETURNING in sql
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostWithVotesResponse)
def get_post(id: int, db: Session = Depends(get_db), cur_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    # print(post)
    vote_count = func.count(models.Post.id)
    query_res = db.query(models.Post, vote_count.label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    post = query_res[0]
    votes = query_res[1]
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    if post.owner_id == cur_user.id:
        return {"Post": post, "votes": votes}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"User {cur_user.id} is not authorized to see post by user {post.owner_id}")


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
    if query.first().owner_id == cur_user.id:
        query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform requested action")


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
    if query.first().owner_id == cur_user.id:
        query.update(post.dict(), synchronize_session=False)
        db.commit()
        # conn.commit()
        return query.first()
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform requested action")
