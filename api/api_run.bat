call ..\.venv\Scripts\activate
uvicorn api:app --host 0.0.0.0 --port 10001 --reload
pause