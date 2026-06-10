import csv
from io import BytesIO, StringIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import select
from sqlalchemy.orm import Session
from xlsxwriter import Workbook

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.transaction import Transaction
from app.models.user import User

router = APIRouter()


@router.get("/{report_type}")
def export_report(report_type: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.scalars(select(Transaction).order_by(Transaction.created_at.desc()).limit(1000)).all()
    if report_type == "csv":
        return _csv(rows)
    if report_type == "excel":
        return _excel(rows)
    if report_type == "pdf":
        return _pdf(rows)
    raise HTTPException(status_code=400, detail="Unsupported report type")


def _csv(rows):
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["reference", "amount", "branch", "status", "transaction_time"])
    for tx in rows:
        writer.writerow([tx.reference, tx.amount, tx.branch, tx.status, tx.transaction_time.isoformat()])
    return StreamingResponse(iter([buffer.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=fraudguard-report.csv"})


def _excel(rows):
    output = BytesIO()
    workbook = Workbook(output, {"in_memory": True})
    sheet = workbook.add_worksheet("Transactions")
    for col, header in enumerate(["reference", "amount", "branch", "status", "transaction_time"]):
        sheet.write(0, col, header)
    for row_num, tx in enumerate(rows, start=1):
        sheet.write(row_num, 0, tx.reference)
        sheet.write(row_num, 1, float(tx.amount))
        sheet.write(row_num, 2, tx.branch or "")
        sheet.write(row_num, 3, tx.status)
        sheet.write(row_num, 4, tx.transaction_time.isoformat())
    workbook.close()
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=fraudguard-report.xlsx"})


def _pdf(rows):
    output = BytesIO()
    pdf = canvas.Canvas(output, pagesize=letter)
    pdf.drawString(40, 750, "FraudGuard Transaction Report")
    y = 720
    for tx in rows[:35]:
        pdf.drawString(40, y, f"{tx.reference} | IDR {float(tx.amount):,.0f} | {tx.branch or '-'} | {tx.status}")
        y -= 18
    pdf.save()
    output.seek(0)
    return StreamingResponse(output, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=fraudguard-report.pdf"})
