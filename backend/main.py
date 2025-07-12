from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .vector_service import VectorService
from .heidi_service import HeidiService
from .models import SearchRequest, SearchResponse, HeidiRequest, HeidiResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global vector service instance
vector_service = None
heidi_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the application lifespan"""
    global vector_service, heidi_service
    
    # Startup
    logger.info("Starting up application...")
    vector_service = VectorService()
    heidi_service = HeidiService()
    
    # Initialize ChromaDB and process PDFs
    await vector_service.initialize()
    await vector_service.process_pdfs()
    
    # Initialize Heidi service (authenticate)
    await heidi_service.authenticate()
    
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

@app.post("/ask-heidi", response_model=HeidiResponse)
async def ask_heidi_endpoint(request: HeidiRequest):
    """
    Process medical notes with Heidi AI to extract drugs and create summaries with vector search context
    
    Flow:
    1. Send medical notes to Heidi to extract drug names
    2. Vector search for chunks related to the extracted drugs
    3. Send drug info + context chunks to Heidi for final summary
    4. Return the comprehensive response
    """
    if not vector_service or not vector_service.is_initialized():
        raise HTTPException(status_code=503, detail="Vector service is not ready")
    
    if not heidi_service:
        raise HTTPException(status_code=503, detail="Heidi service is not ready")
    
    try:
        processing_steps = []
        
        # Step 1: Extract drug names using Heidi
        processing_steps.append("Extracting drug names from medical text using Heidi AI")
        extracted_drugs = await heidi_service.extract_drugs(request.content)
        processing_steps.append(f"Extracted {len(extracted_drugs)} drugs: {', '.join(extracted_drugs) if extracted_drugs else 'None'}")
        
        # Step 2: Vector search for drug-related information
        vector_results = []
        if extracted_drugs:
            processing_steps.append("Searching vector database for drug-related information")
            
            # Create search queries for each drug
            for drug in extracted_drugs:
                try:
                    search_query = f"{drug} antibiotic medication dosage indication contraindication allergy"
                    results = await vector_service.search(
                        query=search_query,
                        n_results=3  # Get 3 results per drug
                    )
                    vector_results.extend(results)
                    processing_steps.append(f"Found {len(results)} context chunks for {drug}")
                except Exception as e:
                    logger.warning(f"Vector search failed for drug {drug}: {str(e)}")
        
        # Step 3: Create final summary using Heidi with context
        processing_steps.append("Generating final drug summary with context using Heidi AI")
        context_chunks = [result.content for result in vector_results[:10]]  # Limit to top 10 chunks
        final_summary = await heidi_service.create_drug_summary(extracted_drugs, context_chunks)
        processing_steps.append("Summary generation completed")
        
        return HeidiResponse(
            message="Medical text processed successfully with Heidi AI and vector search",
            extracted_drugs=extracted_drugs,
            vector_context=vector_results[:5],  # Return top 5 for response
            final_summary=final_summary or "No summary could be generated",
            processing_steps=processing_steps
        )
        
    except Exception as e:
        logger.error(f"Ask Heidi endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
