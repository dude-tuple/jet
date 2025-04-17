__all__ = [
    "router"
]

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from models.base import get_db
from services import GitHubWebhookService
from utils import verify_github_signature
from validators.webhook import GitHubWebhook

router = APIRouter()



@router.post("/webhook")
async def receive_webhook(
    payload: GitHubWebhook,
    request: Request,
    db: Session = Depends(get_db),
    x_hub_signature_256: str = Header(None),
):
    raw_body = await request.body()

    if not verify_github_signature("your-secret", raw_body, x_hub_signature_256):
        raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        result = GitHubWebhookService(db).handle(payload)
        return JSONResponse(content={"status": "ok", "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
