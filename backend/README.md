# Portfolio Backend API

A clean FastAPI backend for the portfolio website.

## Project Structure

```
backend/
 ├── main.py          # FastAPI application entry point
 ├── models.py        # Pydantic models for validation
 ├── routes.py        # API routes
 ├── config.py        # Configuration settings
 ├── .env             # Environment variables
 └── requirements.txt # Python dependencies
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   The `.env` file is already created with default settings. You can modify it if needed.

## Running the Server

### Using uvicorn directly:

```bash
cd backend
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

### With custom host and port:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Options explained:
- `main:app` - refers to the `app` object in `main.py`
- `--reload` - enables auto-reload on code changes (useful for development)
- `--host 127.0.0.1` - makes server accessible on localhost
- `--port 8000` - specifies the port (default is 8000)

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Endpoints

### GET /
Root endpoint to check if API is running.

**Response:**
```json
{
  "message": "Portfolio API is running",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### POST /api/contact

Submit a contact form message.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "This is a test message with at least 10 characters"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Message received successfully",
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "message": "This is a test message with at least 10 characters"
  }
}
```

**Error Response (422) - Validation Error:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "message"],
      "msg": "Value error, Message must be at least 10 characters long",
      "input": "short"
    }
  ]
}
```

## Testing

You can test the API using:
1. **Swagger UI** at http://127.0.0.1:8000/docs (interactive testing)
2. **curl**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/api/contact" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "message": "This is a test message"
     }'
   ```

## Features

- ✅ FastAPI framework
- ✅ Swagger/OpenAPI documentation
- ✅ Pydantic validation
- ✅ CORS middleware enabled
- ✅ Environment variable configuration
- ✅ Clean project structure

