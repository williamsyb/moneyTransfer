from .app_factory import make_app
import uvicorn

app = make_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
