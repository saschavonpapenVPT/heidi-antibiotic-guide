from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SearchRequest(BaseModel):
    """Request model for vector search"""
    query: str = Field(..., description="The search query")
    n_results: int = Field(default=5, ge=1, le=20, description="Number of results to return")

class SearchResult(BaseModel):
    """Individual search result"""
    content: str = Field(..., description="The content chunk")
    source: str = Field(..., description="Source document name")
    distance: float = Field(..., description="Similarity distance (lower is more similar)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class SearchResponse(BaseModel):
    """Response model for vector search"""
    results: List[SearchResult] = Field(..., description="List of search results")

class ProcessingResult(BaseModel):
    """Result of PDF processing operation"""
    message: str = Field(..., description="Processing status message")
    successful: int = Field(..., description="Number of successfully processed files")
    failed: int = Field(default=0, description="Number of failed files")
    details: List[str] = Field(default_factory=list, description="Processing details")

class HeidiRequest(BaseModel):
    """Request model for Heidi ask-heidi endpoint"""
    content: str = Field(..., description="Medical notes/text to process")

class DrugExtraction(BaseModel):
    """Model for drug extraction from Heidi"""
    drugs: List[str] = Field(default_factory=list, description="List of extracted drug names")
    raw_response: str = Field(..., description="Raw response from Heidi")

class HeidiResponse(BaseModel):
    """Response model for Heidi ask-heidi endpoint"""
    message: str = Field(..., description="Status message")
    extracted_drugs: List[str] = Field(default_factory=list, description="Drugs extracted by Heidi")
    vector_context: List[SearchResult] = Field(default_factory=list, description="Related vector search results")
    final_summary: str = Field(..., description="Final drug summary from Heidi")
    processing_steps: List[str] = Field(default_factory=list, description="Processing steps taken")
