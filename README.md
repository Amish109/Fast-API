
# To Run server 
# uvicorn app.main:app --reload
# app.main means:
# app → folder
# main.py → file
# app → FastAPI instance in that file


app/
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── company.py
│   ├── employee.py


from app.models import User, Company, Employee
"# Fast-API" 
