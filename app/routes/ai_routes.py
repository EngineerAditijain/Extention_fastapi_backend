from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.ai_service import generate_response
from app.services.ai_service import list_models
from app.auth import get_current_user
from app import models, schemas
from typing import List
router = APIRouter(prefix="/ai", tags=["AI"])


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ask", response_model=schemas.ChatResponse)
def ask_ai(
    request: schemas.ChatCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    try:
        # 1️⃣ Call Geminilist_models
        # list_models()
        print(request.prompt)
        ai_output = generate_response(request.prompt)

        # 2️⃣ Get logged-in user
        user = db.query(models.User).filter(
            models.User.email == current_user
        ).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 3️⃣ Save history
        history = models.RequestHistory(
            user_id=user.id,
            input_code=request.prompt,
            response_text=ai_output
        )

        new_chat = models.ChatHistory(
          user_id=user.id,
          prompt=request.prompt,
          response=ai_output
        )

        db.add(history)
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)

        # 4️⃣ Return response
        # return {"response": ai_output}
        return new_chat

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history",response_model=List[schemas.ChatResponse])
def get_history(db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)):
    user = db.query(models.User).filter(
            models.User.email == current_user
        ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    chats = db.query(models.ChatHistory).filter(models.ChatHistory.user_id == user.id).order_by(models.ChatHistory.created_at.desc()).all()
    return chats