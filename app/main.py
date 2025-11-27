from fastapi import FastAPI
from .login.router import router as login_router
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ProSiga Auth API", description="API dedicada para autenticação.")

origins = ["*"]

# Adiciona o Middleware com suporte a preview deployments da Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)

@app.get("/")
def health_check():
    return {"status": "fine"}