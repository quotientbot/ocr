up:
	uvicorn app.main:app --port 6969 --host 0.0.0.0 --reload

prod:
	uvicorn app.main:app --port 6969 --host 0.0.0.0