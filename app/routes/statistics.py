import pandas as pd
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.database import SessionLocal
from app.models.experience_db import ExperienceDB
from app.models.experience_logs import ExperienceLog

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):
    most_accessed = db.query(
        ExperienceDB.title, func.count(ExperienceLog.id).label("access_count")
    ).join(ExperienceLog, ExperienceLog.experience_id == ExperienceDB.id)\
     .group_by(ExperienceDB.title)\
     .order_by(func.count(ExperienceLog.id).desc())\
     .limit(5)\
     .all()

    by_category = db.query(
        ExperienceDB.category, func.count(ExperienceDB.id).label("count")
    ).group_by(ExperienceDB.category).all()

    total_experiences = db.query(func.count(ExperienceDB.id)).scalar()

    return {
        "most_accessed_experiences": most_accessed,
        "experiences_by_category": by_category,
        "total_experiences": total_experiences,
    }


@router.get("/statistics/report")
def generate_report(db: Session = Depends(get_db), report_type: str = "excel"):
    # Dados de exemplo
    most_accessed = db.query(
        ExperienceDB.title, func.count(ExperienceLog.id).label("access_count")
    ).join(ExperienceLog, ExperienceLog.experience_id == ExperienceDB.id)\
     .group_by(ExperienceDB.title)\
     .order_by(func.count(ExperienceLog.id).desc())\
     .all()

    df = pd.DataFrame(most_accessed, columns=["Experience", "Access Count"])

    # Geração do relatório
    if report_type == "excel":
        file_path = "statistics_report.xlsx"
        df.to_excel(file_path, index=False)
    else:  # PDF
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors

        file_path = "statistics_report.pdf"
        pdf = SimpleDocTemplate(file_path)
        table_data = [["Experience", "Access Count"]] + most_accessed
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        pdf.build([table])

    return FileResponse(file_path, media_type="application/octet-stream", filename=file_path)
