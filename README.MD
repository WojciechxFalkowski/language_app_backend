Install python version 3
Check python --version -> 3
Check python Environment path
Check pip
Install uvicorn -> pip install uvicorn
pip install -r requirements.txt

command to start project in /backend -> uvicorn main:app --reload
localhost:8000
deta deploy - deploy project



docker build -t language_app_backend .
docker run -p 8000:8000 language_app_backend 