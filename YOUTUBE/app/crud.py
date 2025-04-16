from app.schema import Note, NoteCreate, YouTubeSummary, YouTubeSummaryCreate, Bookmark, BookmarkCreate
from app.db import db, fix_mongo_ids
import uuid
import httpx
import os
from typing import Optional, List
from youtube_transcript_api import YouTubeTranscriptApi
from bson import ObjectId

# Centralized OpenAI API configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

async def create_note(note_data: NoteCreate) -> Note:
    """
    Create a new note and save it to MongoDB
    """
    note = Note(content=note_data.content)
    return await db.engine.save(note)

async def fetch_youtube_transcript(video_id: str) -> Optional[str]:
    """
    Fetch transcript from a YouTube video using youtube-transcript-api
    """
    try:
        # This library is synchronous, so run in a thread pool
        import asyncio
        loop = asyncio.get_event_loop()
        transcript_list = await loop.run_in_executor(
            None, lambda: YouTubeTranscriptApi.get_transcript(video_id)
        )
        transcript = " ".join([item['text'] for item in transcript_list])
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {str(e)}")
        return None

async def make_openai_request(messages: list, max_tokens: int = 500) -> Optional[str]:
    """
    Make a generic OpenAI API request with error handling
    """
    if not OPENAI_API_KEY:
        print("OpenAI API key is not set")
        return None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OPENAI_API_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": max_tokens
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                print(f"OpenAI API Error: {response.status_code} - {response.text}")
                return None
    
    except Exception as e:
        print(f"Request to OpenAI failed: {e}")
        return None

async def generate_summary_with_llm(transcript: str, video_id: str) -> str:
    """
    Generate a summary using OpenAI's GPT model
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes YouTube video transcripts."},
        {"role": "user", "content": f"Please summarize the following YouTube video transcript in about 250 words:\n\n{transcript}"}
    ]
    
    summary = await make_openai_request(messages)
    return summary or f"Failed to generate summary for video {video_id}"

async def create_youtube_summary(summary_data: YouTubeSummaryCreate) -> dict:
    try:
        # Extract video ID from URL
        video_id = None
        if "v=" in summary_data.url:
            video_id = summary_data.url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in summary_data.url:
            video_id = summary_data.url.split("youtu.be/")[1].split("?")[0]
        else:
            video_id = summary_data.url

        # Fetch real transcript
        transcript = await fetch_youtube_transcript(video_id)
        if not transcript:
            transcript = f"No transcript available for video {video_id}."

        # Generate summary using LLM
        summary = await generate_summary_with_llm(transcript, video_id)

        youtube_summary = YouTubeSummary(url=summary_data.url, summary=summary)
        saved_summary = await db.engine.save(youtube_summary)

        # Return the saved summary with fixed IDs
        return fix_mongo_ids({
            "id": str(getattr(saved_summary, "id", None)),
            "url": saved_summary.url,
            "summary": saved_summary.summary
        })
    except Exception as e:
        print(f"Error creating summary: {str(e)}")
        return {
            "url": summary_data.url,
            "summary": f"Error creating summary: {str(e)}"
        }

async def get_youtube_summaries() -> list[dict]:
    """
    Get all YouTube summaries
    """
    try:
        summaries = await db.engine.find(YouTubeSummary)
        return fix_mongo_ids([
            {
                "id": str(getattr(s, "id", None)),
                "url": s.url,
                "summary": s.summary
            }
            for s in summaries
        ])
    except Exception as e:
        print(f"Error fetching summaries: {str(e)}")
        return []

async def get_youtube_summary(summary_id: str) -> dict:
    """
    Get a specific YouTube summary by ID
    """
    try:
        summary = await db.engine.find_one(YouTubeSummary, YouTubeSummary.id == summary_id)
        if summary:
            return fix_mongo_ids({
                "id": str(getattr(summary, "id", None)),
                "url": summary.url,
                "summary": summary.summary
            })
        return None
    except Exception as e:
        print(f"Error fetching summary {summary_id}: {str(e)}")
        return None

from bson import ObjectId

async def delete_youtube_summary(summary_id: str) -> bool:
    """
    Delete a YouTube summary by ID
    """
    try:
        # Convert summary_id to ObjectId for MongoDB/ODMantic
        try:
            obj_id = ObjectId(summary_id)
        except Exception as e:
            print(f"Invalid summary_id format: {summary_id}")
            return False

        summary = await db.engine.find_one(YouTubeSummary, YouTubeSummary.id == obj_id)
        if summary:
            await db.engine.delete(summary)
            print(f"Deleted summary with ID: {summary_id}")
            return True
        else:
            print(f"No summary found with ID: {summary_id}")
            return False
    except Exception as e:
        print(f"Error deleting summary {summary_id}: {str(e)}")
        return False

async def create_bookmark(bookmark_data: BookmarkCreate) -> dict:
    """
    Create a new bookmark
    """
    try:
        # Convert BookmarkCreate to Bookmark model
        bookmark = Bookmark(
            title=bookmark_data.title,
            url=str(bookmark_data.url),
            description=bookmark_data.description,
            tags=bookmark_data.tags or []
        )
        
        # Save to database
        saved_bookmark = await db.engine.save(bookmark)
        
        # Return fixed mongo IDs
        return fix_mongo_ids({
            "id": str(getattr(saved_bookmark, "id", None)),
            "title": saved_bookmark.title,
            "url": saved_bookmark.url,
            "description": saved_bookmark.description,
            "tags": saved_bookmark.tags,
            "created_at": saved_bookmark.created_at.isoformat()
        })
    except Exception as e:
        print(f"Error creating bookmark: {str(e)}")
        raise

async def get_bookmarks(tag: Optional[str] = None) -> List[dict]:
    """
    Retrieve bookmarks, optionally filtered by tag
    """
    try:
        # If tag is provided, filter bookmarks
        if tag:
            bookmarks = await db.engine.find(Bookmark, Bookmark.tags.contains(tag))
        else:
            bookmarks = await db.engine.find(Bookmark)
        
        # Convert to list of dicts with fixed mongo IDs
        return fix_mongo_ids([
            {
                "id": str(getattr(b, "id", None)),
                "title": b.title,
                "url": b.url,
                "description": b.description,
                "tags": b.tags,
                "created_at": b.created_at.isoformat()
            }
            for b in bookmarks
        ])
    except Exception as e:
        print(f"Error fetching bookmarks: {str(e)}")
        return []

async def delete_bookmark(bookmark_id: str) -> bool:
    """
    Delete a bookmark by its ID
    """
    try:
        # Convert bookmark_id to ObjectId
        try:
            obj_id = ObjectId(bookmark_id)
        except Exception:
            print(f"Invalid bookmark_id format: {bookmark_id}")
            return False

        # Find and delete the bookmark
        bookmark = await db.engine.find_one(Bookmark, Bookmark.id == obj_id)
        if bookmark:
            await db.engine.delete(bookmark)
            print(f"Deleted bookmark with ID: {bookmark_id}")
            return True
        else:
            print(f"No bookmark found with ID: {bookmark_id}")
            return False
    except Exception as e:
        print(f"Error deleting bookmark {bookmark_id}: {str(e)}")
        return False