import database as _database
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException
from passlib.hash import bcrypt 
from jwt import encode
import models
import schemas

JWT_SECRET = "dkfjgkdj234nfrjtkjn_!w23424hjk"

def create_db():
    return models.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally: 
        db.close()

async def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email==email).first()

async def create_user(user: schemas.UserRequest, db: Session):
    # check for valid email
    try:
        is_valid = validate_email(email = user.email)
        email = is_valid.email
    except EmailNotValidError: 
        raise HTTPException(status=400, detail="email is incorrect")
    
    # encrypt the password (hash)
    hashed_password = bcrypt.hash(user.password)

    # create the user model to be saved to database
    user_object = models.User(
        email = email, 
        # group = user.group,
        hashed_password = hashed_password
        )
    
    # save the user to database
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    return user_object

async def create_token(user: models.User):
    # convert user model to user schema
    user_schema = schemas.UserResponse.from_orm(user)
    # convert object to a dictionary
    user_dict = user_schema.dict()
    del user_dict['created_at']
    # creating a token
    token = encode(user_dict, JWT_SECRET)
    return {"access_token": token, "token_type": "bearer"}