import uvicorn
from decouple import config

from app.app import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(config("PORT", default=80)))
