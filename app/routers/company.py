from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/company", tags=["Company"])

# Dependency to get DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.CompanyResponse)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    return crud.create_company(db, company)

@router.get("/", response_model=list[schemas.CompanyResponse])
def list_companies(db: Session = Depends(get_db)):
    return crud.get_all_companies(db)

@router.get("/{company_id}", response_model=schemas.CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    return crud.get_company_by_id(db, company_id)

@router.put("/{company_id}", response_model=schemas.CompanyResponse)
def update_company(company_id: int, company: schemas.CompanyUpdate, db: Session = Depends(get_db)):
    return crud.update_company(db, company_id, company)

@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    return crud.delete_company(db, company_id)
