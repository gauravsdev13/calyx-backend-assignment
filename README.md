# calyx-backend-assignment

## Architecture Overview

1. FastAPI handles HTTP routing and request/response validation.
2. Pydantic Schemas (schemas.py) define the structure and validation rules for API input/ 
   output.
3. SQLAlchemy Models (models.py) define the database tables and columns.
4. CRUD Layer (crud.py) contains all database interaction logic, keeping business logic 
   separate from routing.
5. Utils (utils.py) contains reusable logic such as scoring functions and proof generation.

### Scoring Logic
Raw values are passed through a sigmoid scoring function, then adjusted using a category-based multiplier:
- emissions: +5%
- water: no change
- waste: -5%

### Core Data Flow
1. Request hits an endpoint (e.g., /submit).
2. Data is validated by a Pydantic schema.
3. Endpoint calls a CRUD function, which:
    - Uses utility functions for scoring and proof.
    - Creates and saves SQLAlchemy model instances.
4. Response is serialized using a Pydantic schema.

### Tech Stack
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- asyncio

### How to Run

1. Open a terminal and navigate to the backend folder:

cd backend

2. Make sure your `.env` file contains a valid local PostgreSQL connection string for `DATABASE_URL`.

3. Start the FastAPI server:

uvicorn app.main:app --reload

4. API Documentation:
Once the server is running, access the interactive API docs at:  
- Swagger UI: [http://localhost:8000/docs]

5. To run tests:

py -m unittest tests/test_scoring.py
