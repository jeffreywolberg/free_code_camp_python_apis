from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
  prefix="/users",
  tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    hashed_pwd = utils.hash_pwd(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user) # add new post to db
    db.commit() # commit changes
    db.refresh(new_user) # retrieve new post we just created and store it in new_post. Equivalent of doing RETURNING in sql
    return new_user

@router.get('/{id}', response_model=schemas.UserReponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"User with id: {id} does not exist")
    
    return user