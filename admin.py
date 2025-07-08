from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Depends
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
      <head><title>Bot Admin</title></head>
      <body>
        <h1>Welcome to Your Bot Admin Panel</h1>
        <p>Go to /users or /settings</p>
      </body>
    </html>
    """

@app.get("/users")
async def get_users():
    return {"users": ["user1", "user2", "user3"]}

@app.get("/settings")
async def get_settings():
    return {"setting_1": True, "setting_2": "value"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username, "joined": u.joined_at} for u in users]
