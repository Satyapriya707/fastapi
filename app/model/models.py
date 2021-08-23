from pydantic import BaseModel
from typing import List

class listOfAllFiles(BaseModel):
    directoryPath: str
    listOfFiles: List[str]
