from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn
from multiprocessing import Process, Manager
from threading import Thread

app = FastAPI()


@app.post("/total_files")
def number_of_files(path: str):
    files = next(os.walk(path))[2]
    file_count = len(files)
    return file_count


@app.post("/file_names_async")
async def name_of_all_files_async(path: List[str]):
    names_async = {}
    for folder in path:
        files = next(os.walk(folder))[2]
        names_async[folder] = files
    return names_async


def all_files_mp(folder: str, names_mp):
    files = next(os.walk(folder))[2]
    names_mp[folder] = files

@app.post("/file_names_multiprocessing")
def name_of_all_files_multiprocessing(path: List[str]):
    manager = Manager()
    names_mp = manager.dict()
    processes = []
    for p in path:
        pr = Process(target=all_files_mp, args=(p, names_mp))
        processes.append(pr)
        pr.start()
    for pr in processes:
        pr.join()
    return names_mp


def all_files_mt(folder: str, names_mt):
    files = next(os.walk(folder))[2]
    names_mt[folder] = files

@app.post("/file_names_multithreading")
def name_of_all_files_multithreading(path: List[str]):
    manager = Manager()
    names_mt = manager.dict()
    processes = []
    for p in path:
        pr = Process(target=all_files_mt, args=(p, names_mt))
        processes.append(pr)
        pr.start()
    for pr in processes:
        pr.join()
    return names_mt

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)



        
