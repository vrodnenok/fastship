from http.client import HTTPException
import fastapi as _fastapi
import schemas
import services
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

app = _fastapi.FastAPI()

@app.get("/")
async def index():
    return

@app.get("/v1/api/users/current", response_model = schemas.UserResponse)
async def current_user(user: schemas.UserResponse = _fastapi.Depends(services.current_user)):
    return user

@app.post("/v1/api/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: Session = _fastapi.Depends(services.get_db)):
    db_user = await services.login(username=form_data.username, 
        password = form_data.password, db = db)
    
    # invalid login throws exception
    if not db_user:
        raise _fastapi.HTTPException(status_code=401, detail = "Wrong login credentioals.")
    return await services.create_token(db_user)

@app.post("/v1/api/users")
async def register_user (user:schemas.UserRequest, db: Session = _fastapi.Depends(services.get_db)): 
    # = _fastapi.Depends(services.get_db())):
    # check if email if already in database
    db_user = await services.get_user_by_email(email=user.email, db = db)
    # if user found throw an exception
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="User already exists!")

    # create user and return token
    db_user = await services.create_user(user = user, db = db)
    return await services.create_token(user = db_user)