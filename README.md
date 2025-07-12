# Docker Compose Project for Medical Document Vector Search

This project provides a FastAPI backend with ChromaDB vector database for processing and searching medical PDF documents.

## Architecture

- **Backend**: FastAPI application with vector search capabilities
- **Database**: ChromaDB vector database for document embeddings
- **Documents**: PDF files in the `references/` directory are automatically processed

## Quick Start

1. **Start the services:**
   ```bash
   docker-compose up --build
   ```

2. **The services will be available at:**
   - Backend API: http://localhost:8000
   - ChromaDB: http://localhost:8001
   - API Documentation: http://localhost:8000/docs

## Features

### Automatic PDF Processing
- All PDF files in the `references/` directory are automatically processed on startup
- Each PDF gets its own ChromaDB collection
- Documents are chunked using LangChain's RecursiveCharacterTextSplitter
- Text embeddings are generated using sentence-transformers

### API Endpoints

- `GET /` - Health check
- `GET /health` - Service health status
- `POST /vector/search` - Search across all PDF collections
- `POST /vector/process-pdfs` - Manually trigger PDF processing
- `GET /vector/collections` - List all available collections

### Search Example

```bash
curl -X POST "http://localhost:8000/vector/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "antibiotic resistance treatment",
       "n_results": 5
     }'
```

## Development

### Adding New PDFs
1. Place PDF files in the `references/` directory
2. Restart the services or call the `/vector/process-pdfs` endpoint

### Environment Variables
- `CHROMA_HOST`: ChromaDB host (default: chromadb)
- `CHROMA_PORT`: ChromaDB port (default: 8001)

### Docker Services
- **backend**: FastAPI application
- **chromadb**: ChromaDB vector database with persistent storage

## Technical Details

- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Chunk Size**: 1000 characters with 200 character overlap
- **Search Method**: Cosine similarity across all collections
- **Storage**: Persistent ChromaDB storage in Docker volume
