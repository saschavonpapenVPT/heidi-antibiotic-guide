# Vector Database Implementation Guide

## Overview

This implementation provides comprehensive vector database functionality for processing and searching medical PDF documents. Each PDF in the `references/` directory is automatically chunked, vectorized, and stored in its own ChromaDB collection for efficient similarity search.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │◄──►│    Backend      │◄──►│   ChromaDB      │
│   (Next.js)     │    │   (FastAPI)     │    │  (Vector Store) │
│   Port 3000     │    │   Port 8000     │    │   Port 8001     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                               ▼
                       ┌─────────────────┐
                       │   References    │
                       │   (PDF Files)   │
                       └─────────────────┘
```

## Features

### 1. PDF Processing
- **Automatic Text Extraction**: Uses PyPDF2 to extract text from PDF documents
- **Intelligent Chunking**: Uses LangChain's RecursiveCharacterTextSplitter with 1000 character chunks and 200 character overlap
- **Separate Collections**: Each PDF gets its own ChromaDB collection for organized storage
- **Metadata Tracking**: Stores source file, chunk index, and other metadata

### 2. Vector Embeddings
- **Model**: Uses `sentence-transformers/all-MiniLM-L6-v2` for generating embeddings
- **Efficiency**: Lightweight model optimized for semantic similarity
- **Consistency**: All documents use the same embedding model for comparable results

### 3. Search Capabilities
- **Cross-Collection Search**: Search across all PDF collections simultaneously
- **Similarity Ranking**: Results ranked by cosine similarity distance
- **Metadata Filtering**: Results include source file and chunk information
- **Configurable Results**: Adjustable number of returned results

## API Endpoints

### Core Vector Endpoints

#### `POST /vector/process-pdfs`
Processes all PDFs in the references directory.

**Response:**
```json
{
  "message": "PDF processing completed. 1/1 files processed successfully.",
  "results": {
    "Clinical Practice Guidelines _ Antimicrobial guidelines.pdf": true
  },
  "total_processed": 1,
  "successful": 1
}
```

#### `POST /vector/search`
Search across all PDF collections.

**Request:**
```json
{
  "query": "antibiotic resistance treatment",
  "n_results": 5
}
```

**Response:**
```json
{
  "results": [
    {
      "collection": "pdf_clinical_practice_guidelines_antimicrobial_guidelines",
      "document": "Antibiotic resistance is a major concern...",
      "source_file": "Clinical Practice Guidelines _ Antimicrobial guidelines.pdf",
      "metadata": {
        "source_file": "Clinical Practice Guidelines _ Antimicrobial guidelines.pdf",
        "chunk_index": 15,
        "chunk_size": 982
      },
      "distance": 0.234
    }
  ],
  "total_results": 1
}
```

#### `GET /vector/collections`
Get information about all collections.

**Response:**
```json
{
  "collections": [
    {
      "name": "pdf_clinical_practice_guidelines_antimicrobial_guidelines",
      "document_count": 45,
      "source_file": "Clinical Practice Guidelines _ Antimicrobial guidelines.pdf",
      "metadata": {
        "source_file": "Clinical Practice Guidelines _ Antimicrobial guidelines.pdf"
      }
    }
  ],
  "total_collections": 1
}
```

### Enhanced Integration

#### `POST /ask-heidi-enhanced`
Combines Heidi AI processing with vector search.

**Request:**
```json
{
  "content": "Patient has pneumonia, allergic to penicillin, weight 70kg",
  "include_vector_search": true,
  "search_query": "pneumonia antibiotic alternatives penicillin allergy"
}
```

**Response:**
```json
{
  "message": "Content processed successfully with Heidi AI",
  "received_content": "Patient has pneumonia, allergic to penicillin...",
  "extractions": {
    "antibiotics": "No specific antibiotics mentioned",
    "patient_weight": "70kg",
    "allergies": "Allergic to penicillin",
    "diagnosis": "Pneumonia"
  },
  "vector_results": [
    {
      "collection": "pdf_clinical_practice_guidelines_antimicrobial_guidelines",
      "document": "For patients allergic to penicillin with pneumonia...",
      "source_file": "Clinical Practice Guidelines _ Antimicrobial guidelines.pdf",
      "metadata": {...},
      "distance": 0.156
    }
  ],
  "recommendations": "Found 3 relevant guideline sections from Clinical Practice Guidelines _ Antimicrobial guidelines.pdf. Consider reviewing these guidelines for treatment recommendations."
}
```

## Management Scripts

### Initialization
```bash
# Process all PDFs and create vector databases
./scripts/vector.sh init
```

### Testing
```bash
# Test vector search functionality
./scripts/vector.sh test
```

### Information
```bash
# Show collections and document counts
./scripts/vector.sh info
```

### Rebuild
```bash
# Rebuild backend and reinitialize databases
./scripts/vector.sh rebuild
```

## File Structure

```
backend/
├── vector_service.py          # Main vector database service
├── init_vector_db.py          # Initialization script
├── test_vector_search.py      # Testing script
├── main.py                    # FastAPI app with vector endpoints
└── requirements.txt           # Updated with vector dependencies

references/
└── *.pdf                      # PDF files to be processed

scripts/
└── vector.sh                  # Vector database management script
```

## Technical Details

### ChromaDB Configuration
- **Host**: `vectordb` (Docker service name)
- **Port**: 8000 (internal), 8001 (external)
- **Persistent Storage**: Docker volume `chroma_data`
- **Collections**: Automatically created with naming pattern `pdf_{sanitized_filename}`

### Text Processing Pipeline
1. **PDF Text Extraction**: PyPDF2 extracts raw text
2. **Text Chunking**: RecursiveCharacterTextSplitter creates overlapping chunks
3. **Embedding Generation**: SentenceTransformer creates vector embeddings
4. **Storage**: ChromaDB stores embeddings with metadata
5. **Search**: Cosine similarity search across collections

### Error Handling
- Graceful handling of PDF extraction failures
- Collection existence checks
- Comprehensive logging for debugging
- Fallback responses for search failures

## Performance Considerations

### Embedding Model
- **Model Size**: ~90MB download on first use
- **Speed**: ~1000 chunks/second on typical hardware
- **Memory**: ~500MB RAM usage for model

### Storage
- **Text**: Original text stored for retrieval
- **Embeddings**: 384-dimensional vectors (1.5KB per chunk)
- **Metadata**: JSON metadata per chunk

### Scaling
- **Horizontal**: Add more ChromaDB instances
- **Vertical**: Increase memory for larger collections
- **Caching**: Embedding model cached in memory

## Security and Privacy

### Data Protection
- PDFs processed locally within Docker containers
- No external API calls for embeddings
- Embeddings stored in local ChromaDB instance

### Access Control
- Internal Docker network communication
- No direct external access to ChromaDB
- FastAPI endpoints provide controlled access

## Troubleshooting

### Common Issues

#### "No collections found"
```bash
# Ensure PDFs exist and process them
ls references/
./scripts/vector.sh init
```

#### "ChromaDB connection failed"
```bash
# Check if vectordb service is running
docker-compose ps
./scripts/logs.sh vectordb
```

#### "PDF extraction failed"
- Ensure PDF files are not corrupted
- Check file permissions in Docker container
- Review backend logs for specific errors

### Debugging Commands
```bash
# Check backend logs
./scripts/logs.sh backend

# Check vectordb logs  
./scripts/logs.sh vectordb

# Test vector service directly
docker-compose exec backend python test_vector_search.py
```

## Future Enhancements

### Potential Improvements
1. **Incremental Updates**: Only process changed PDFs
2. **Advanced Chunking**: Semantic chunking based on document structure
3. **Multiple Models**: Support for different embedding models
4. **Caching**: Redis cache for frequent searches
5. **Filtering**: Advanced metadata filtering capabilities
6. **Analytics**: Search analytics and usage metrics

### Integration Ideas
1. **Real-time Processing**: Watch folder for new PDFs
2. **OCR Support**: Process scanned PDFs with OCR
3. **Document Classification**: Automatic categorization of PDFs
4. **Relevance Scoring**: ML-based relevance improvements
5. **Multi-modal Search**: Support for images and tables

---

This vector database implementation provides a solid foundation for medical document search and retrieval, designed to scale with your application's needs while maintaining performance and accuracy.
