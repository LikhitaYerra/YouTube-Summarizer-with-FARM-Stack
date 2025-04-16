YouTube Summarizer
The YouTube Summarizer is a FastAPI-based web application that generates concise summaries of YouTube videos using their transcripts and OpenAI's GPT-3.5-turbo model. It also supports note-taking and bookmark management, making it a versatile tool for content creators, researchers, and students. The application uses MongoDB for persistent storage and includes a mock database for testing, ensuring robust and scalable performance.
Features

YouTube Video Summarization: Automatically fetches video transcripts and generates summaries using OpenAI's language model.
Bookmark Management: Create, retrieve, and delete bookmarks with titles, URLs, descriptions, and tags.
Note Creation: Store and manage simple text notes.
RESTful API: Provides endpoints for CRUD operations on summaries, bookmarks, and notes.
MongoDB Integration: Persistent storage with ODMantic ORM, with a mock database fallback for testing.
Asynchronous Architecture: Leverages FastAPI and Motor for efficient, non-blocking operations.
CORS Support: Enables integration with frontend applications.

Project Structure
youtube-summarizer/
├── app/
│   ├── __init__.py
│   ├── crud.py           # CRUD operations for notes, summaries, and bookmarks
│   ├── db.py             # Database setup and mock engine
│   ├── router.py         # API route definitions
│   ├── schema.py         # Data models and validation schemas
│   └── static/           # Static files for frontend (e.g., index.html)
├── main.py               # FastAPI application entry point
├── requirements.txt      # Project dependencies
├── .env.example          # Example environment variables
└── README.md             # Project documentation

Installation
Prerequisites

Python 3.8+
MongoDB (or use the mock database for testing)
OpenAI API key
YouTube Transcript API (no key required)

Steps

Clone the Repository:
git clone https://github.com/yourusername/youtube-summarizer.git
cd youtube-summarizer


Set Up a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Configure Environment Variables: Copy .env.example to .env and update with your credentials:
cp .env.example .env

Edit .env:
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
OPENAI_API_KEY=your-openai-api-key


Run the Application:
uvicorn main:app --reload

The API will be available at http://localhost:8000.

Access the Frontend (if available): Open http://localhost:8000/static/index.html in your browser.


API Endpoints



Method
Endpoint
Description



POST
/notes/
Create a new note


POST
/youtube-summary/
Generate a YouTube video summary


GET
/youtube-summaries/
List all YouTube summaries


GET
/youtube-summary/{id}
Get a specific YouTube summary


DELETE
/youtube-summaries/{id}
Delete a YouTube summary


POST
/bookmarks/
Create a new bookmark


GET
/bookmarks/
List bookmarks (optional tag filter)


DELETE
/bookmarks/{bookmark_id}
Delete a bookmark


Explore the API documentation at http://localhost:8000/docs.
Usage

Summarize a YouTube Video: Send a POST request to /youtube-summary/ with a JSON body:
{
    "url": "https://www.youtube.com/watch?v=video_id"
}


Create a Bookmark: Send a POST request to /bookmarks/:
\{
    "title": "Example Bookmark",
    "url": "https://example.com",
    "description": "A useful resource",
    "tags": ["learning", "tech"]
}


Retrieve Bookmarks: Send a GET request to /bookmarks/?tag=learning to filter by tag.


Testing
The application includes a mock database (MockEngine) for testing without a MongoDB instance. To use it, ensure MONGODB_URI is not set or invalid, and the app will fallback to the mock database.
Run tests (if implemented) with:
pytest

Limitations

Requires YouTube videos to have transcripts available.
Depends on OpenAI API, which incurs costs and requires a valid key.
Mock database lacks persistence and advanced query support.
Limited to common YouTube URL formats for video ID parsing.
No user authentication (suitable for single-user or prototype use).

Future Improvements

Add user authentication (e.g., JWT or OAuth2).
Implement caching for transcripts and summaries.
Develop a dedicated frontend (e.g., React).
Support multiple summary lengths or custom prompts.
Enhance URL parsing for broader compatibility.
Add rate limiting and MongoDB indexes.

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a feature branch (git checkout -b feature/new-feature).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature/new-feature).
Open a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or feedback, please open an issue or contact [your email or preferred contact method].

Built with ❤️ by [Your Name/Team]
