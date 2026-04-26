from fastapi import FastAPI
from .database import engine
from .models import Base
from app.routes import auth_routes,ai_routes
app = FastAPI(title="AI Dev Assistant API")
app.include_router(auth_routes.router)
app.include_router(ai_routes.router)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}