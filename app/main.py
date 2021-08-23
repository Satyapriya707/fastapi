from fastapi import FastAPI
import uvicorn
from routers.count import fileCount
from routers.loop import filesUsingLoop
from routers.concurrency import multiprocessing, multithreading, asynchronous

app = FastAPI()

app.include_router(fileCount.router)
app.include_router(filesUsingLoop.router)
app.include_router(multiprocessing.router)
app.include_router(multithreading.router)
app.include_router(asynchronous.router)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='127.0.0.1', reload=True)

