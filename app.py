import fastapi as _fastapi
import schemas
import services
from sqlalchemy.orm import Session

app = _fastapi.FastAPI()

@app.get("/")
async def index():
    return

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