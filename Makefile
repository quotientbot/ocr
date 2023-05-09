up:
	uvicorn app.main:app --port 8000 --host 0.0.0.0 --reload

prod:
	uvicorn app.main:app --port 8000 --host 0.0.0.0