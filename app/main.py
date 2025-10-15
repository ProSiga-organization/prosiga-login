from fastapi import FastAPI
from .login.router import router as login_router
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ProSiga Auth API", description="API dedicada para autenticação.")

app.include_router(login_router)

@app.get("/")
def health_check():
    return {"status": "fine"}