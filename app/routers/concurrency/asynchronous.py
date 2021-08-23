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
import asyncio

router = APIRouter(tags = ["List of Files Using Concurrency"])

async def allFilesAsync(folder: str, namesAsync = List):
    files = next(os.walk(folder))[2]
    temp = {"directoryPath": folder, "listOfFiles":files}
    namesAsync.append(listOfAllFiles(**temp))

@router.get("/namesOfFilesAsyncio", response_model=List[listOfAllFiles], summary="Find Names of All Files Using Asyncio", status_code=status.HTTP_202_ACCEPTED, responses={404: {"model": Message}})
async def nameOfAllFilesMultithreading(path: List[str]= Query(..., example = ["C:\Program Files","E:\Python"], max_length=150)):
    namesAsync = []
    tasks = []
    for p in path:
        if not os.path.isdir(p):
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"The path {p} does not exist"})
        task = allFilesAsync(p,namesAsync)
        tasks.append(task)
    await asyncio.gather(*tasks) 
    return namesAsync
