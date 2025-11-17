from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import frontend, api, admin
import uvicorn

app = FastAPI(title="Version API sympa ^^")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(frontend.router)
app.include_router(api.router)
app.include_router(admin.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)