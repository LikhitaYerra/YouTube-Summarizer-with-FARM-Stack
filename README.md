
# YouTube Summarizer

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.11-green)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.0%2B-brightgreen)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

The **YouTube Summarizer** is a FastAPI-based web application that generates concise summaries of YouTube videos using their transcripts and OpenAI's GPT-3.5-turbo model. It also supports note-taking and bookmark management, making it a versatile tool for content creators, researchers, and students. The application uses MongoDB for persistent storage and includes a mock database for testing, ensuring robust and scalable performance.

## Features

- **YouTube Video Summarization**: Automatically fetches video transcripts and generates summaries using OpenAI's language model.
- **Bookmark Management**: Create, retrieve, and delete bookmarks with titles, URLs, descriptions, and tags.
- **Note Creation**: Store and manage simple text notes.
- **RESTful API**: Provides endpoints for CRUD operations on summaries, bookmarks, and notes.
- **MongoDB Integration**: Persistent storage with ODMantic ORM, with a mock database fallback for testing.
- **Asynchronous Architecture**: Leverages FastAPI and Motor for efficient, non-blocking operations.
- **CORS Support**: Enables integration with frontend applications.

## Project Structure

```
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
```

## Installation

### Prerequisites

- Python 3.8+
- MongoDB (or use the mock database for testing)
- OpenAI API key
- YouTube Transcript API (no key required)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/youtube-summarizer.git
   cd youtube-summarizer
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and update with your credentials:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
   OPENAI_API_KEY=your-openai-api-key
   ```

5. **Run the Application**:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

6. **Access the Frontend** (if available):
   Open `http://localhost:8000/static/index.html` in your browser.

## API Endpoints

| Method | Endpoint                     | Description                              |
|--------|------------------------------|------------------------------------------|
| POST   | `/notes/`                    | Create a new note                        |
| POST   | `/youtube-summary/`          | Generate a YouTube video summary         |
| GET    | `/youtube-summaries/`        | List all YouTube summaries               |
| GET    | `/youtube-summary/{id}`      | Get a specific YouTube summary           |
| DELETE | `/youtube-summaries/{id}`    | Delete a YouTube summary                 |
| POST   | `/bookmarks/`                | Create a new bookmark                    |
| GET    | `/bookmarks/`                | List bookmarks (optional tag filter)     |
| DELETE | `/bookmarks/{bookmark_id}`   | Delete a bookmark                        |

Explore the API documentation at `http://localhost:8000/docs`.

## Usage

1. **Summarize a YouTube Video**:
   Send a POST request to `/youtube-summary/` with a JSON body:
   ```json
   {
       "url": "https://www.youtube.com/watch?v=video_id"
   }
   ```

2. **Create a Bookmark**:
   Send a POST request to `/bookmarks/`:
   ```json
   \{
       "title": "Example Bookmark",
       "url": "https://example.com",
       "description": "A useful resource",
       "tags": ["learning", "tech"]
   }
   ```

3. **Retrieve Bookmarks**:
   Send a GET request to `/bookmarks/?tag=learning` to filter by tag.

## Testing

The application includes a mock database (`MockEngine`) for testing without a MongoDB instance. To use it, ensure `MONGODB_URI` is not set or invalid, and the app will fallback to the mock database.

Run tests (if implemented) with:
```bash
pytest
```

## Limitations

- Requires YouTube videos to have transcripts available.
- Depends on OpenAI API, which incurs costs and requires a valid key.
- Mock database lacks persistence and advanced query support.
- Limited to common YouTube URL formats for video ID parsing.
- No user authentication (suitable for single-user or prototype use).

## Future Improvements

- Add user authentication (e.g., JWT or OAuth2).
- Implement caching for transcripts and summaries.
- Develop a dedicated frontend (e.g., React).
- Support multiple summary lengths or custom prompts.
- Enhance URL parsing for broader compatibility.
- Add rate limiting and MongoDB indexes.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


