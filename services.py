import database as _database
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException
from passlib.hash import bcrypt 
from jwt import encode, decode
import models
import schemas
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

JWT_SECRET = "dkfjgkdj234nfrjtkjn_!w23424hjk"

def create_db():
    return models.Base.metadata.create_all(bind=_database.engine)

# create_db()

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally: 
        db.close()

oath2schema = OAuth2PasswordBearer("/v1/api/login")


async def current_user(db: Session = Depends(get_db), token: str = Depends(oath2schema)):
    try:
        payload = decode(token, JWT_SECRET, algorithms=["HS256"])
        # get user by id from payoad
        db_user = db.query(models.User).get(payload["id"])
    except:
        raise HTTPException(status_code=401, detail="Wrong credentials...")

    # if all okay return user
    return schemas.UserResponse.from_orm(db_user)


async def get_user(username: str, db: Session):
    return db.query(models.User).filter(models.User.username==username).first()

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
        username = user.username,
        group = user.group,
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

async def login(username: str, password: str, db: Session):
    db_user = await get_user(username = username, db = db)
    
    # return False if no user or password found
    if not db_user:
        return False
    if not db_user.verify_password(password = password):
        return False
    return db_user