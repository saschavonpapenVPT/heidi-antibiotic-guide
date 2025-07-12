import os
import logging
from typing import List, Dict, Any, Optional
import asyncio
from pathlib import Path

import chromadb
import PyPDF2
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .models import SearchResult, ProcessingResult

logger = logging.getLogger(__name__)

class VectorService:
    """Service for managing vector operations with ChromaDB"""
    
    def __init__(self):
        self.client = None
        self.embedding_model = None
        self.text_splitter = None
        self.collections = {}
        self.initialized = False
        
        # Configuration for local development
        self.references_dir = Path("references")
        
    async def initialize(self) -> None:
        """Initialize ChromaDB connection and embedding model"""
        try:
            # Initialize ChromaDB client for local development
            self.client = chromadb.PersistentClient(path="./chroma_db")
            logger.info("Connected to local ChromaDB")
            
            # Initialize embedding model
            logger.info("Loading embedding model...")
            self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            logger.info("Embedding model loaded successfully")
            
            # Initialize text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", ". ", " ", ""]
            )
            
            self.initialized = True
            logger.info("Vector service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize vector service: {str(e)}")
            raise
    
    def is_initialized(self) -> bool:
        """Check if the service is properly initialized"""
        return self.initialized and self.client is not None
    
    async def process_pdfs(self) -> ProcessingResult:
        """Process all PDFs in the references directory"""
        if not self.is_initialized():
            raise RuntimeError("Vector service not initialized")
        
        if not self.references_dir.exists():
            logger.warning(f"References directory not found: {self.references_dir}")
            return ProcessingResult(
                message="References directory not found",
                successful=0,
                failed=0
            )
        
        pdf_files = list(self.references_dir.glob("*.pdf"))
        if not pdf_files:
            logger.info("No PDF files found in references directory")
            return ProcessingResult(
                message="No PDF files found in references directory",
                successful=0,
                failed=0
            )
        
        successful = 0
        failed = 0
        details = []
        
        for pdf_file in pdf_files:
            try:
                await self._process_single_pdf(pdf_file)
                successful += 1
                details.append(f"Successfully processed: {pdf_file.name}")
                logger.info(f"Successfully processed: {pdf_file.name}")
            except Exception as e:
                failed += 1
                error_msg = f"Failed to process {pdf_file.name}: {str(e)}"
                details.append(error_msg)
                logger.error(error_msg)
        
        total_files = len(pdf_files)
        message = f"PDF processing completed. {successful}/{total_files} files processed successfully."
        
        return ProcessingResult(
            message=message,
            successful=successful,
            failed=failed,
            details=details
        )
    
    async def _process_single_pdf(self, pdf_path: Path) -> None:
        """Process a single PDF file"""
        # Extract text from PDF
        text_content = self._extract_text_from_pdf(pdf_path)
        if not text_content.strip():
            raise ValueError("No text content extracted from PDF")
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text_content)
        if not chunks:
            raise ValueError("No chunks created from PDF text")
        
        # Create collection name from filename (sanitized)
        collection_name = self._sanitize_collection_name(pdf_path.stem)
        
        # Handle existing collections by deleting and recreating them
        try:
            # Try to delete existing collection first
            self.client.delete_collection(name=collection_name)
            logger.info(f"Deleted existing collection '{collection_name}'")
        except ValueError:
            # Collection doesn't exist, which is fine
            pass
        except Exception as e:
            logger.warning(f"Could not delete existing collection '{collection_name}': {str(e)}")
        
        # Create new collection
        try:
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"source": pdf_path.name}
            )
            logger.info(f"Created collection '{collection_name}'")
        except Exception as e:
            raise ValueError(f"Failed to create collection '{collection_name}': {str(e)}")
        
        # Generate embeddings and store chunks
        embeddings = self.embedding_model.encode(chunks).tolist()
        
        # Prepare documents for insertion
        ids = [f"{collection_name}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "source": pdf_path.name,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]
        
        # Add documents to collection
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )
        
        # Store collection reference
        self.collections[collection_name] = collection
        
        logger.info(f"Added {len(chunks)} chunks to collection '{collection_name}'")
    
    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text content from a PDF file"""
        text_content = ""
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_content += page_text + "\n"
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num + 1} of {pdf_path.name}: {str(e)}")
                        continue
                        
        except Exception as e:
            raise ValueError(f"Failed to read PDF file {pdf_path.name}: {str(e)}")
        
        return text_content
    
    def _sanitize_collection_name(self, name: str) -> str:
        """Sanitize collection name for ChromaDB"""
        # Replace spaces and special characters with underscores
        sanitized = "".join(c if c.isalnum() else "_" for c in name)
        # Remove consecutive underscores and strip
        sanitized = "_".join(filter(None, sanitized.split("_")))
        # Ensure it starts with a letter or underscore
        if sanitized and not (sanitized[0].isalpha() or sanitized[0] == "_"):
            sanitized = f"doc_{sanitized}"
        return sanitized.lower()
    
    async def search(self, query: str, n_results: int = 5) -> List[SearchResult]:
        """Search across all collections"""
        if not self.is_initialized():
            raise RuntimeError("Vector service not initialized")
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        
        # Get all collections
        all_collections = self.client.list_collections()
        
        if not all_collections:
            logger.warning("No collections found")
            return []
        
        all_results = []
        
        # Search each collection
        for collection_info in all_collections:
            try:
                collection = self.client.get_collection(collection_info.name)
                
                # Query the collection
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=min(n_results, 10)  # Limit per collection
                )
                
                # Process results
                if results['documents'] and results['documents'][0]:
                    for i, (doc, distance, metadata) in enumerate(zip(
                        results['documents'][0],
                        results['distances'][0],
                        results['metadatas'][0]
                    )):
                        all_results.append(SearchResult(
                            content=doc,
                            source=metadata.get('source', 'Unknown'),
                            distance=distance,
                            metadata=metadata
                        ))
                        
            except Exception as e:
                logger.error(f"Error searching collection {collection_info.name}: {str(e)}")
                continue
        
        # Sort by distance and return top results
        all_results.sort(key=lambda x: x.distance)
        return all_results[:n_results]
    
    async def list_collections(self) -> List[Dict[str, Any]]:
        """List all available collections"""
        if not self.is_initialized():
            raise RuntimeError("Vector service not initialized")
        
        collections = self.client.list_collections()
        return [
            {
                "name": col.name,
                "metadata": col.metadata
            }
            for col in collections
        ]
