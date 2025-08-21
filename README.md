A FastAPI-based backend application for uploading, parsing, and managing files with progress tracking using SQLite as the database.

Features
File upload with progress tracking

Support for CSV, Excel, PDF, and text files

CRUD operations for files

Real-time progress updates

Background file processing

SQLite database for data persistence

Installation
Clone the repository:

bash
git clone <repository-url>
cd file-parser-api
Install dependencies:

bash
pip install fastapi uvicorn sqlalchemy aiofiles python-multipart pandas openpyxl pdfplumber
Run the application:

bash
uvicorn main:app --reload
API Endpoints
1. Upload a File
Endpoint: POST /files

Request:

bash
curl -X POST "http://localhost:8000/files" \
     -F "file=@example.csv"
Response:

json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "example.csv",
  "status": "uploading",
  "progress": 50.0,
  "created_at": "2023-11-10T12:34:56.789Z",
  "updated_at": "2023-11-10T12:34:56.789Z"
}
2. Check Upload/Processing Progress
Endpoint: GET /files/{file_id}/progress

Request:

bash
curl -X GET "http://localhost:8000/files/a1b2c3d4-e5f6-7890-abcd-ef1234567890/progress"
Response (during upload):

json
{
  "file_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "uploading",
  "progress": 50.0
}
Response (when ready):

json
{
  "file_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "ready",
  "progress": 100.0
}
3. Get Parsed File Content
Endpoint: GET /files/{file_id}

Request:

bash
curl -X GET "http://localhost:8000/files/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
Response (if still processing):

json
{
  "message": "File upload or processing in progress. Please try again later."
}
Response (if ready - CSV example):

json
{
  "data": [
    {
      "Name": "John",
      "Age": 30,
      "City": "New York"
    },
    {
      "Name": "Jane",
      "Age": 25,
      "City": "Los Angeles"
    }
  ]
}
4. List All Files
Endpoint: GET /files

Request:

bash
curl -X GET "http://localhost:8000/files"
Response:

json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "filename": "example.csv",
    "status": "ready",
    "progress": 100.0,
    "created_at": "2023-11-10T12:34:56.789Z",
    "updated_at": "2023-11-10T12:35:02.123Z"
  },
  {
    "id": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
    "filename": "report.pdf",
    "status": "processing",
    "progress": 30.0,
    "created_at": "2023-11-10T12:36:15.456Z",
    "updated_at": "2023-11-10T12:36:18.789Z"
  }
]
5. Delete a File
Endpoint: DELETE /files/{file_id}

Request:

bash
curl -X DELETE "http://localhost:8000/files/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
Response:

json
{
  "message": "File deleted successfully"
}
File Format Support
CSV Files: Parsed into JSON array of objects

Excel Files: Parsed into JSON array of objects

PDF Files: Text extraction with page-by-page content

Other Files: Treated as text files

Database Schema
The application uses SQLite with the following schema:

files table:

id: UUID string (primary key)

filename: Original filename

status: Current status (uploading, processing, ready, failed)

progress: Progress percentage (0-100)

file_path: Path to the stored file

parsed_data: JSON content of parsed file

created_at: Timestamp of creation

updated_at: Timestamp of last update

Error Handling
The API returns appropriate HTTP status codes:

200: Success

202: Processing in progress

404: File not found

500: Internal server error
