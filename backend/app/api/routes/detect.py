from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.routes.transactions import _process_file
from app.core.database import get_db

router = APIRouter()


@router.post("/detect", include_in_schema=False)
async def legacy_detect(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await _process_file(file, db, None)
