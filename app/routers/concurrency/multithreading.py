from typing import Optional, List
from fastapi import FastAPI, Query, APIRouter, status
from pydantic import BaseModel, DirectoryPath
import os
import uvicorn
from multiprocessing import Process, Manager
from threading import Thread
from model.errorMessage import Message
from model.models import listOfAllFiles
from fastapi.responses import JSONResponse

router = APIRouter(tags = ["List of Files Using Concurrency"])

def allFilesMT(folder: str, namesMT):
    files = next(os.walk(folder))[2]
    namesMT[folder] = files

@router.get("/namesOfFilesMultithreading", response_model=List[listOfAllFiles], summary="Find Names of All Files Using Multithreading", status_code=status.HTTP_202_ACCEPTED, responses={404: {"model": Message}})
def nameOfAllFilesMultithreading(path: List[str]= Query(..., example = ["C:\Program Files","E:\Python"], max_length=150)):
    manager = Manager()
    namesMT = manager.dict()
    threads = []
    for p in path:
        if not os.path.isdir(p):
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"The path {p} does not exist"})
        thr = Thread(target=allFilesMT, args=(p, namesMT))
        threads.append(thr)
        thr.start()
    for thr in threads:
        thr.join()
    filesList = []
    for paths in namesMT:
        tempList = {"directoryPath": paths, "listOfFiles":namesMT[paths]}
        filesList.append(listOfAllFiles(**tempList))
    return filesList
