gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app -b "0.0.0.0:8888"




