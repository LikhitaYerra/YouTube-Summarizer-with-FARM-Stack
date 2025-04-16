from fastapi import APIRouter, HTTPException, Query
from app.schema import NoteCreate, YouTubeSummaryCreate, BookmarkCreate
from app.crud import (
    create_note, 
    create_youtube_summary, 
    get_youtube_summaries, 
    get_youtube_summary, 
    delete_youtube_summary,
    create_bookmark, 
    get_bookmarks, 
    delete_bookmark
)
from typing import List, Optional

router = APIRouter()

@router.post("/notes/")
async def create_new_note(note_data: NoteCreate):
    """
    Create a new note
    """
    return await create_note(note_data)

@router.post("/youtube-summary/")
async def create_summary(summary_data: YouTubeSummaryCreate):
    """
    Create a YouTube video summary
    """
    return await create_youtube_summary(summary_data)

@router.get("/youtube-summaries/")
async def list_summaries():
    """
    Get all YouTube summaries
    """
    return await get_youtube_summaries()

@router.get("/youtube-summary/{id}")
async def get_summary(id: str):
    """
    Get a specific YouTube summary by ID
    """
    summary = await get_youtube_summary(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary

@router.delete("/youtube-summaries/{id}")
async def remove_summary(id: str):
    """
    Delete a YouTube summary by ID
    """
    success = await delete_youtube_summary(id)
    if not success:
        raise HTTPException(status_code=404, detail="Summary not found")
    return {"message": "Summary deleted successfully"}

@router.post("/bookmarks/", response_model=dict, tags=["bookmarks"])
async def create_new_bookmark(bookmark_data: BookmarkCreate):
    """
    Create a new bookmark
    
    - **title**: A descriptive title for the bookmark (required)
    - **url**: The URL to be bookmarked (required)
    - **description**: Optional description of the bookmark
    - **tags**: Optional list of tags to categorize the bookmark
    """
    try:
        return await create_bookmark(bookmark_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/bookmarks/", response_model=List[dict], tags=["bookmarks"])
async def list_bookmarks(
    tag: Optional[str] = Query(None, description="Filter bookmarks by tag")
):
    """
    Retrieve bookmarks
    
    - **tag**: Optional tag to filter bookmarks
    """
    return await get_bookmarks(tag)

@router.delete("/bookmarks/{bookmark_id}", tags=["bookmarks"])
async def remove_bookmark(bookmark_id: str):
    """
    Delete a bookmark by its ID
    
    - **bookmark_id**: The unique identifier of the bookmark to delete
    """
    success = await delete_bookmark(bookmark_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return {"message": "Bookmark deleted successfully"}


