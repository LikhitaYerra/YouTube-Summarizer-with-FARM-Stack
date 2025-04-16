from odmantic import Model, Field as OdmanticField
from pydantic import BaseModel, HttpUrl, Field as PydanticField, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class Note(Model):
    content: str

class NoteCreate(BaseModel):
    content: str

class MindmapNode(BaseModel):
    name: str
    children: Optional[List['MindmapNode']] = None

class YouTubeSummary(Model):
    url: str
    summary: str

class YouTubeSummaryCreate(BaseModel):
    url: str

class BookmarkCreate(BaseModel):
    """Schema for creating a new bookmark"""
    title: str = PydanticField(..., min_length=1, max_length=200, description="Title of the bookmark")
    url: HttpUrl = PydanticField(..., description="URL of the bookmark")
    description: Optional[str] = PydanticField(None, max_length=500, description="Optional description of the bookmark")
    tags: Optional[List[str]] = PydanticField(default_factory=list, description="Optional tags for the bookmark")

class Bookmark(Model):
    """MongoDB model for storing bookmarks"""
    title: str
    url: str
    description: Optional[str] = OdmanticField(default=None)
    tags: List[str] = OdmanticField(default_factory=list)
    created_at: datetime = OdmanticField(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
