from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .vector_service import VectorService
from .models import SearchRequest, SearchResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global vector service instance
vector_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the application lifespan"""
    global vector_service
    
    # Startup
    logger.info("Starting up application...")
    vector_service = VectorService()
    
    # Initialize ChromaDB and process PDFs
    await vector_service.initialize()
    await vector_service.process_pdfs()
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")

app = FastAPI(
    title="Medical Document Vector Search API",
    description="API for searching through medical PDF documents using vector embeddings",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for your use case
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Medical Document Vector Search API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if vector_service and vector_service.is_initialized():
        return {"status": "healthy", "message": "Vector service is ready"}
    else:
        raise HTTPException(status_code=503, detail="Vector service is not ready")

@app.post("/vector/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """Search across all PDF collections using vector similarity"""
    if not vector_service or not vector_service.is_initialized():
        raise HTTPException(status_code=503, detail="Vector service is not ready")
    
    try:
        results = await vector_service.search(
            query=request.query,
            n_results=request.n_results
        )
        return SearchResponse(results=results)
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/vector/process-pdfs")
async def process_pdfs():
    """Manually trigger PDF processing"""
    if not vector_service:
        raise HTTPException(status_code=503, detail="Vector service is not ready")
    
    try:
        result = await vector_service.process_pdfs()
        return result
    except Exception as e:
        logger.error(f"PDF processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")

@app.get("/vector/collections")
async def list_collections():
    """List all available collections"""
    if not vector_service or not vector_service.is_initialized():
        raise HTTPException(status_code=503, detail="Vector service is not ready")
    
    try:
        collections = await vector_service.list_collections()
        return {"collections": collections}
    except Exception as e:
        logger.error(f"Error listing collections: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list collections: {str(e)}")
