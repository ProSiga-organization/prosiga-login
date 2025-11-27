from fastapi import FastAPI
from .login.router import router as login_router
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ProSiga Auth API", description="API dedicada para autenticação.")


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|.*\.vercel\.app)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)

@app.get("/")
def health_check():
    return {"status": "fine"}