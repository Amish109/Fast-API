from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
# Company CRUD operations
def create_company(db: Session, company_data: schemas.CompanyCreate):
    company = models.Company(name=company_data.name)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

def get_all_companies(db: Session):
    return db.query(models.Company).all()

def get_company_by_id(db: Session, company_id: int):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

def update_company(db: Session, company_id: int, company_data: schemas.CompanyUpdate):
    company = get_company_by_id(db, company_id)
    company.name = company_data.name
    db.commit()
    db.refresh(company)
    return company

def delete_company(db: Session, company_id: int):
    company = get_company_by_id(db, company_id)
    db.delete(company)
    db.commit()
    return {"message": f"Company {company.name} deleted successfully"}


# ------------------------
# ✅ User CRUD
# ------------------------

def create_user(db: Session, user_data: schemas.UserCreate):
    user = models.User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        company_id=user_data.company_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(db: Session, user_id: int, user_data: schemas.UserCreate):
    user = get_user_by_id(db, user_id)
    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    user.company_id = user_data.company_id
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
    return {"message": f"User {user.name} deleted successfully"}

# ------------------------
# ✅ Employee CRUD
# ------------------------
def create_employee(db: Session, employee_data: schemas.EmployeeCreate):
    # ✅ Hash the password
    hashed_pw = hash_password(employee_data.password)

    # ✅ Create User first
    user = models.User(
        name=employee_data.name,
        email=employee_data.email,
        password=hashed_pw,
        role=employee_data.role,
        company_id=employee_data.company_id,
    )
    db.add(user)
    db.flush()  # Get user.id before commit

    # ✅ Create Employee linked to the new user
    employee = models.Employee(
        position=employee_data.position,
        salary=employee_data.salary,
        user_id=user.id
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

def get_all_employees(db: Session):
    return db.query(models.Employee).all()

def get_employee_by_id(db: Session, employee_id: int):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

def update_employee(db: Session, employee_id: int, employee_data: schemas.EmployeeCreate):
    employee = get_employee_by_id(db, employee_id)
    
    # update employee data only (not user creation again)
    employee.position = employee_data.position
    employee.salary = employee_data.salary

    # update linked user data
    user = employee.user
    user.name = employee_data.name
    user.email = employee_data.email
    user.role = employee_data.role
    user.company_id = employee_data.company_id

    db.commit()
    db.refresh(employee)
    return employee

def delete_employee(db: Session, employee_id: int):
    employee = get_employee_by_id(db, employee_id)
    db.delete(employee)
    db.commit()

    # Optionally also delete the linked user
    user = db.query(models.User).filter(models.User.id == employee.user_id).first()
    if user:
        db.delete(user)
        db.commit()

    return {"message": f"Employee {employee.id} (and user) deleted successfully"}