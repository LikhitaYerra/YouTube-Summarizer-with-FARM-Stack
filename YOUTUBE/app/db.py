from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import asyncio
import os
import ssl

# Use environment variable for MongoDB URI to improve security
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://remiuttejitha0719:024iiiSXTJRfOoZY@cluster0.usxr7bp.mongodb.net/")
MONGODB_DB_NAME = "youtube_summaries"

# Mock database for testing
mock_summaries = []
mock_bookmarks = []

class MockEngine:
    async def save(self, document):
        # Handle YouTubeSummary
        if hasattr(document, "__class__") and document.__class__.__name__ == "YouTubeSummary":
            # Generate a simple ID if it doesn't have one
            if not hasattr(document, "id") or not document.id:
                import uuid
                document.id = str(uuid.uuid4())  # <-- Ensure id is a string
            mock_summaries.append(document)
            return document
        
        # Handle Bookmark
        if hasattr(document, "__class__") and document.__class__.__name__ == "Bookmark":
            # Generate a simple ID if it doesn't have one
            if not hasattr(document, "id") or not document.id:
                import uuid
                document.id = str(uuid.uuid4())  # <-- Ensure id is a string
            mock_bookmarks.append(document)
            return document
        
        return document
    
    async def find(self, model):
        if model.__name__ == "YouTubeSummary":
            return mock_summaries
        elif model.__name__ == "Bookmark":
            return mock_bookmarks
        return []
    
    async def find_one(self, model, condition):
        # Handle YouTubeSummary
        if model.__name__ == "YouTubeSummary":
            # Extract the ID from the condition
            summary_id = None
            try:
                # Try to get the ID from different possible condition structures
                if hasattr(condition, "right"):
                    summary_id = condition.right
                elif hasattr(condition, "value"):
                    summary_id = condition.value
                elif isinstance(condition, str):
                    summary_id = condition
                
                # If we found an ID, look for a matching summary
                if summary_id:
                    for summary in mock_summaries:
                        if hasattr(summary, "id") and summary.id == summary_id:
                            return summary
            except Exception as e:
                print(f"Error parsing condition: {str(e)}")
        
        # Handle Bookmark
        if model.__name__ == "Bookmark":
            # Extract the ID from the condition
            bookmark_id = None
            try:
                # Try to get the ID from different possible condition structures
                if hasattr(condition, "right"):
                    bookmark_id = condition.right
                elif hasattr(condition, "value"):
                    bookmark_id = condition.value
                elif isinstance(condition, str):
                    bookmark_id = condition
                
                # If we found an ID, look for a matching bookmark
                if bookmark_id:
                    for bookmark in mock_bookmarks:
                        if hasattr(bookmark, "id") and bookmark.id == bookmark_id:
                            return bookmark
            except Exception as e:
                print(f"Error parsing condition: {str(e)}")
        
        return None
    
    async def delete(self, document):
        # Handle YouTubeSummary
        if hasattr(document, "__class__") and document.__class__.__name__ == "YouTubeSummary":
            global mock_summaries
            mock_summaries = [s for s in mock_summaries if s.id != document.id]
            return True
        
        # Handle Bookmark
        if hasattr(document, "__class__") and document.__class__.__name__ == "Bookmark":
            global mock_bookmarks
            mock_bookmarks = [b for b in mock_bookmarks if b.id != document.id]
            return True
        
        return False

class Database:
    client: AsyncIOMotorClient = None
    engine: AIOEngine = None

db = Database()

def setup_mock_db():
    """Set up a mock database for testing"""
    db.engine = MockEngine()
    print("Using mock database for testing")

async def connect_to_mongo():
    """
    Establish a connection to MongoDB with comprehensive error handling
    """
    try:
        # Remove manual SSL context and connection_options
        db.client = AsyncIOMotorClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000
        )

        # Test the connection with a ping
        await db.client.admin.command('ping')
        
        # Initialize ODMantic engine
        db.engine = AIOEngine(client=db.client, database=MONGODB_DB_NAME)
        
        print("Successfully connected to MongoDB")
        return True

    except Exception as e:
        print(f"Detailed MongoDB Connection Error: {type(e).__name__}")
        print(f"Error Details: {str(e)}")
        
        # Fallback to mock database
        setup_mock_db()
        return False

# Automatically set up mock database if connection fails
async def initialize_database():
    connected = await connect_to_mongo()
    if not connected:
        print("Falling back to mock database")
        setup_mock_db()

async def close_mongo_connection():
    """
    Safely close MongoDB connection
    """
    try:
        # Check if client exists and is not None
        if db.client is not None:
            db.client.close()
            print("Closed MongoDB connection")
        
        # Reset client and engine
        db.client = None
        db.engine = None
    except Exception as e:
        print(f"Error closing MongoDB connection: {str(e)}")

from bson import ObjectId

def fix_mongo_ids(obj):
    """Recursively convert ObjectId fields to strings for JSON serialization."""
    if isinstance(obj, list):
        return [fix_mongo_ids(item) for item in obj]
    elif isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if isinstance(v, ObjectId):
                new_obj[k] = str(v)
            else:
                new_obj[k] = fix_mongo_ids(v)
        return new_obj
    else:
        return obj
