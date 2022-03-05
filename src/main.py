if __name__ == "__main__":
    import uvicorn
    from decouple import config
    from app.app import app

    uvicorn.run(app, host="0.0.0.0", port=int(config("PORT", default=80)))
