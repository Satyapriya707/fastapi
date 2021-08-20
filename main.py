from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

@app.post("/total_files")
def number_of_files(path: str):
    files = next(os.walk(path))[2]
    file_count = len(files)
    return file_count

@app.post("/file_names")
def name_of_all_files(path: List[str]):
    names = {}
    for folder in path:
        files = next(os.walk(folder))[2]
        names[folder] = files
    return names

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)





##[
##  "C:/Users/satya/Desktop/jupyter", "C:/Users/satya/Desktop/jupyter/practice"
##]
