from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
    # prefix allows routes below to not have to enter the prefix each time for the route
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), cur_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if not post_query.first():
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No post exists with id {vote.post_id}")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id ==
                                         vote.post_id, models.Vote.user_id == cur_user.id)
    fetched_vote = vote_query.first()
    if vote.dir == 1:
        if fetched_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {cur_user.id} has already voted on post {fetched_vote.post_id}")
        try:
            new_vote = models.Vote(user_id=cur_user.id, post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            return {"msg": "Successfully added vote"}
        except Exception as e:
            return {"Failed to add vote": e}
    elif vote.dir == 0:
        if not fetched_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Cannot find vote for user {cur_user.id} and post_id {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"msg": "Successfully deleted vote"}
    else:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                            detail=f"Nothing is implemented for editing this vote in the requested way")
