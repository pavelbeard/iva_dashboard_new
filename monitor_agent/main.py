import uvicorn

from core.core import app
from core.routers import data_router

app.include_router(data_router.router)


@app.get("/")
async def root():
    return {"message": "root"}


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
