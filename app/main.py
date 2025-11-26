from fastapi import FastAPI
from .login.router import router as login_router
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ProSiga Auth API", description="API dedicada para autenticação.")

origins = [
    "http://localhost:3000",
    "http://0.0.0.0:3000",
    "http://127.0.0.1:3000",
    "https://prosiga-frontend.vercel.app",
]

# Adiciona o Middleware com suporte a preview deployments da Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Permite todos os subdomínios da Vercel
    allow_origins=origins,       
    allow_credentials=True,      
    allow_methods=["*"],         
    allow_headers=["*"],         
)

app.include_router(login_router)

@app.get("/")
def health_check():
    return {"status": "fine"}