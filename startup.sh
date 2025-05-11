# python -m uvicorn main:app --host 0.0.0.0
# gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
fastapi run --workers 4 main.py