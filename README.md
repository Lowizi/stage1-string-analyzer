# Stage 1 String Analyzer Service

## Setup
1. Clone repo: `git clone https://github.com/yourusername/stage1-string-analyzer.git`
2. Navigate: `cd stage1-string-analyzer`
3. Create venv: `python -m venv venv`
4. Activate: `source venv/bin/activate`
5. Install deps: `pip install -r requirements.txt`
6. Migrate: `python manage.py migrate`
7. Run: `python manage.py runserver`

## Dependencies
- Django
- djangorestframework

## Environment Variables
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL URL (for deployment)

## API Endpoints
- POST /strings/
- GET /strings/<string_value>/
- GET /strings/?<filters>
- GET /strings/filter-by-natural-language/?query=<query>
- DELETE /strings/<string_value>/delete/

Url = https://stage1-string-analyzer.onrender.com
