from app.api import User
from app.models import UserModel


async def get_user(db, username: str):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    return user


async def create_user(db, user: UserModel):
    db.add(user)
    db.commit()
    db.refresh(user)
    return User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
    )
