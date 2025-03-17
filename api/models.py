from pydantic import BaseModel
from typing import Optional, Union
from pathlib import Path

class SRSDocument(BaseModel):
    content: Union[str, Path]  # Can accept either string content or file path
    project_name: Optional[str] = None

class SummaryResponse(BaseModel):
    project_summary: str
    status: str = "success"