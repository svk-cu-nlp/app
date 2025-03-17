from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import google.generativeai as genai
from llama_parse import LlamaParse
import os
import logging
import base64
import asyncio
import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/summary", tags=["Summary"])

# Initialize LlamaParse
parser = LlamaParse(
    api_key=os.getenv('LLAMA_PARSE_API_KEY'),
    result_type="markdown",
    num_workers=4,
    verbose=True,
    language="en",
)

# Initialize Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

@router.post("/generate")
async def generate_summary(request: Dict[str, Any]):
    try:
        # Log the incoming request
        logger.debug("Processing new summary generation request")
        
        # Verify content exists in request
        if 'content' not in request:
            raise HTTPException(status_code=400, detail="No content provided")

        # Save the PDF content temporarily
        temp_pdf_path = "temp_document.pdf"
        try:
            # Decode base64 content if it's base64 encoded
            if isinstance(request['content'], str):
                try:
                    pdf_content = base64.b64decode(request['content'])
                except:
                    pdf_content = request['content'].encode('latin-1')
            else:
                pdf_content = request['content']

            # Save temporary file
            with open(temp_pdf_path, 'wb') as f:
                f.write(pdf_content)
            
            logger.debug(f"Temporary PDF saved to {temp_pdf_path}")

            # Parse the document using LlamaParse
            try:
                # Use asyncio.get_event_loop().run_until_complete for async operation
                documents = await parser.aload_data(temp_pdf_path)
                logger.debug(f"Successfully parsed document, got {len(documents)} pages")
            except Exception as e:
                logger.error(f"LlamaParse error: {str(e)}")
                raise HTTPException(status_code=500, detail=f"PDF parsing failed: {str(e)}")

            # Combine text from parsed documents
            SRS_text = "\n".join([doc.text for doc in documents])
            
            # Prepare the prompt
            prompt = """
            Analyze the document and make sure that you have not missed any feature or requirements.
            Do not miss any functional, technical or non-functional requirements.
            Finally, just provide a detailed summary of the functionality of the software project.
            """

            # Generate content using Gemini
            response = model.generate_content(
                f"Here is the SRS document content:\n{SRS_text}\n\nPlease accomplish the following task based strictly on the document. Task: {prompt}"
            )

            return {
                "project_summary": response.text,
                "srs_text": SRS_text,  # Include the parsed SRS content in the response
                "status": "success"
            }

        finally:
            # Clean up temporary file
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
                logger.debug("Temporary PDF file cleaned up")

    except Exception as e:
        logger.error(f"Error in generate_summary: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate summary: {str(e)}"
        )