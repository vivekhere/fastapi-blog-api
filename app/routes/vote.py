from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, oauth2, schemas

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("")
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user=Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post does not exist.")

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id,
        models.Vote.post_id == vote.post_id)

    if not vote_query.first():
        vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(vote)
        db.commit()
        return

    vote_query.delete(synchronize_session=False)
    db.commit()
    return
