from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.risk import router as risk_router

app = FastAPI(
    title="ARTech Finance AML Backend",
    description="Yapay zeka tabanlı kara para takip sistemi backend API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # geliştirme aşamasında serbest
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(risk_router, prefix="/api/risk", tags=["Risk"])

@app.get("/")
def root():
    return {
        "message": "ARTech Finance AML Backend çalışıyor."
    }