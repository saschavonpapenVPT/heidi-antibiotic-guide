from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

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
