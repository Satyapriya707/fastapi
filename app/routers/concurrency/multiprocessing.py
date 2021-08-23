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

def allFilesMP(folder: str, namesMP):
    files = next(os.walk(folder))[2]
    namesMP[folder] = files

@router.get("/namesOfFilesMultiprocessing", response_model=List[listOfAllFiles], summary="Find Names of All Files Using Multiprocessing", status_code=status.HTTP_202_ACCEPTED, responses={404: {"model": Message}})
def nameOfAllFilesMultiprocessing(path: List[str]= Query(..., example = ["C:\Program Files","E:\Python"], max_length=150)):
    manager = Manager()
    namesMP = manager.dict()
    processes = []
    for p in path:
        if not os.path.isdir(p):
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"The path {p} does not exist"})
        pr = Process(target=allFilesMP, args=(p, namesMP))
        processes.append(pr)
        pr.start()
    for pr in processes:
        pr.join()
    filesList = []
    for paths in namesMP:
        tempList = {"directoryPath": paths, "listOfFiles":namesMP[paths]}
        filesList.append(listOfAllFiles(**tempList))
    return filesList

