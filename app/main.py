from fastapi import FastAPI
from .login.router import router as login_router
from .database import Base, engine

Base.metadata.create_all(bind=engine) # Garante que o serviço "conhece" as tabelas

app = FastAPI(title="ProSiga Auth API")
app.include_router(login_router)

@app.get("/")
def health_check():
    return {"status": "ok"}