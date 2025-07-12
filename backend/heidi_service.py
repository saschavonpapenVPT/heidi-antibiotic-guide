import httpx
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class HeidiService:
    """Service for interacting with Heidi API"""
    
    def __init__(self):
        # Load API key from environment or use staging key
        self.api_key = "MI0QanRHLm4ovFkBVqcBrx3LCiWLT8eu"  # Staging key from docs
        self.base_url = "https://registrar.api.heidihealth.com/api/v2/ml-scribe/open-api"
        self.jwt_token = None
        self.session_id = None
        
    async def authenticate(self) -> bool:
        """Authenticate with Heidi API and get JWT token"""
        try:
            headers = {
                "Heidi-Api-Key": self.api_key
            }
            
            params = {
                "email": "test@heidihealth.com",
                "third_party_internal_id": "123"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/jwt",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.jwt_token = data.get("token")
                    logger.info("Successfully authenticated with Heidi API")
                    return True
                else:
                    logger.error(f"Authentication failed: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
    
    async def create_session(self) -> bool:
        """Create a new Heidi session"""
        if not self.jwt_token:
            if not await self.authenticate():
                return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.jwt_token}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/sessions",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.session_id = data.get("session_id")
                    logger.info(f"Created Heidi session: {self.session_id}")
                    return True
                else:
                    logger.error(f"Session creation failed: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Session creation error: {str(e)}")
            return False
    
    async def ask_heidi(self, ai_command: str, content: str) -> Optional[str]:
        """Ask Heidi AI assistant with specific command and content"""
        if not self.session_id:
            if not await self.create_session():
                return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.jwt_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "ai_command_text": ai_command,
                "content": content,
                "content_type": "MARKDOWN"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/sessions/{self.session_id}/ask-ai",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    # Log the raw response for debugging
                    logger.info(f"Raw response text: {response.text[:500]}...")
                    
                    # Handle both streamed and regular JSON responses
                    full_response = ""
                    
                    # Try parsing as regular JSON first
                    try:
                        json_data = response.json()
                        if isinstance(json_data, dict):
                            # Check for common response fields
                            if 'response' in json_data:
                                full_response = json_data['response']
                            elif 'data' in json_data:
                                full_response = json_data['data']
                            elif 'content' in json_data:
                                full_response = json_data['content']
                            elif 'message' in json_data:
                                full_response = json_data['message']
                            else:
                                # If it's a simple string response
                                full_response = str(json_data)
                        else:
                            full_response = str(json_data)
                    except json.JSONDecodeError:
                        # Handle as streamed response
                        for line in response.text.split('\n'):
                            if line.strip():
                                try:
                                    data = json.loads(line)
                                    if 'data' in data:
                                        full_response += data['data']
                                    elif 'response' in data:
                                        full_response += data['response']
                                except json.JSONDecodeError:
                                    # If not JSON, treat as plain text
                                    full_response += line + "\n"
                    
                    # If still empty, use the raw response text
                    if not full_response.strip():
                        full_response = response.text
                    
                    logger.info(f"Processed response: {full_response[:200]}...")
                    return full_response.strip()
                else:
                    logger.error(f"Ask Heidi failed: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Ask Heidi error: {str(e)}")
            return None
    
    async def extract_drugs(self, medical_text: str) -> List[str]:
        """Extract drug names from medical text using Heidi"""
        command = """You are a medical AI assistant. Please extract all medication names, drug names, and antibiotic names from the following medical text.
        
        Instructions:
        - Only return the actual drug/medication names mentioned in the text
        - Return them as a simple comma-separated list
        - Include generic names, brand names, and antibiotic names
        - Do not include any other text, explanations, or formatting
        - If no drugs are found, return "none"
        
        Example response: gentamicin, amoxicillin, ciprofloxacin"""
        
        response = await self.ask_heidi(command, medical_text)
        logger.info(f"Heidi drug extraction response: {response}")
        
        if response:
            # Parse the response to extract drug names
            drugs = []
            
            # Clean up the response
            response = response.strip()
            
            # Handle simple cases first
            if response.lower() in ['none', 'no drugs', 'no medications', 'no drugs found']:
                return []
            
            # Try to extract from the full response text
            import re
            
            # First, check if it's already a comma-separated list
            if ',' in response and len(response.split('\n')) <= 2:
                # Simple comma-separated format
                for drug in response.split(','):
                    drug = drug.strip().strip('.-*():')
                    if drug and len(drug) > 2 and not drug.lower() in ['none', 'no', 'not', 'any']:
                        drugs.append(drug.title())
            else:
                # Parse line by line
                lines = response.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                        
                    # Skip common response prefixes
                    if any(line.lower().startswith(prefix) for prefix in [
                        'based on', 'the following', 'here are', 'i found', 'i can identify',
                        'medications mentioned', 'drugs mentioned', 'the medications', 'the drugs',
                        'extracted', 'identified', 'found the following'
                    ]):
                        continue
                    
                    # Look for comma-separated drug names
                    if ',' in line:
                        for drug in line.split(','):
                            drug = drug.strip().strip('.-*():')
                            # Remove common prefixes/suffixes
                            drug = re.sub(r'^(medication|drug|antibiotic):\s*', '', drug, flags=re.IGNORECASE)
                            drug = re.sub(r'\s*(medication|drug|antibiotic)$', '', drug, flags=re.IGNORECASE)
                            if drug and len(drug) > 2 and not drug.lower() in ['none', 'no', 'not', 'any']:
                                drugs.append(drug.title())
                    else:
                        # Single drug per line
                        drug = line.strip('.-*():')
                        drug = re.sub(r'^(medication|drug|antibiotic):\s*', '', drug, flags=re.IGNORECASE)
                        drug = re.sub(r'\s*(medication|drug|antibiotic)$', '', drug, flags=re.IGNORECASE)
                        if drug and len(drug) > 2 and not drug.lower() in ['none', 'no', 'not', 'any']:
                            drugs.append(drug.title())
            
            # Remove duplicates while preserving order
            seen = set()
            unique_drugs = []
            for drug in drugs:
                if drug.lower() not in seen:
                    seen.add(drug.lower())
                    unique_drugs.append(drug)
            
            logger.info(f"Extracted drugs: {unique_drugs}")
            return unique_drugs
        
        logger.warning("No response from Heidi for drug extraction")
        return []
    
    async def create_drug_summary(self, drugs: List[str], context_chunks: List[str]) -> str:
        """Create a summary about drugs using context from vector database"""
        if not drugs:
            return "No drugs were identified in the provided medical text."
        
        # Prepare context from vector chunks
        context = "\n\n".join([f"Context {i+1}: {chunk}" for i, chunk in enumerate(context_chunks)])
        
        drugs_list = ", ".join(drugs)
        
        command = f"""Based on the following medical reference context, provide a brief clinical summary about these medications: {drugs_list}
        
        Include information about:
        - Indications and usage
        - Important considerations or warnings
        - Dosing considerations if mentioned
        - Any contraindications or allergies to be aware of
        
        Keep the summary concise and clinically relevant.
        
        Reference Context:
        {context}"""
        
        medical_text = f"Medications identified: {drugs_list}"
        
        response = await self.ask_heidi(command, medical_text)
        return response or f"Summary for medications: {drugs_list} (context processing completed)"
