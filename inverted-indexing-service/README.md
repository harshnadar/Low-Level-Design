# Inverted Index Service

A Flask-based service that provides text file indexing and searching capabilities using an inverted index data structure.

## Features

- **File Upload**: Upload text files to be indexed
- **Full-Text Search**: Search for terms across all uploaded files
- **File Management**: List and delete indexed files
- **Thread-Safe**: Supports concurrent operations

## Installation

1. Clone the repository:
```bash
cd inverted-index-service
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

```bash
python run.py
```

The service will start on `http://localhost:5000`

## API Endpoints

### Upload File
- **POST** `/api/upload`
- Upload a text file to be indexed
- Body: multipart/form-data with 'file' field

### Search
- **GET** `/api/search?q=<search_term>`
- Search for files containing the specified term

### List Files
- **GET** `/api/files`
- List all indexed files with metadata

### Delete File
- **DELETE** `/api/files/<filename>`
- Delete a file and remove it from the index

## Example Usage

### Upload a file:
```bash
curl -X POST -F "file=@sample.txt" http://localhost:5000/api/upload
```

### Search for a term:
```bash
curl http://localhost:5000/api/search?q=python
```

### List all files:
```bash
curl http://localhost:5000/api/files
```

### Delete a file:
```bash
curl -X DELETE http://localhost:5000/api/files/sample.txt
```

## Testing

Create a sample text file to test:
```bash
echo "This is a sample text file for testing the inverted index service." > sample.txt
```

Then upload and search:
```bash
curl -X POST -F "file=@sample.txt" http://localhost:5000/api/upload
curl http://localhost:5000/api/search?q=inverted
```