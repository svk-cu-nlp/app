from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import google.generativeai as genai
import os
import logging
from ..models import (
    FeatureExtractionRequest,
    FeatureReEvaluationRequest,
    FeatureResponse
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/features", tags=["Features"])

# Initialize Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
thinking_model = genai.GenerativeModel('gemini-2.0-flash')

# Feature extraction prompt
FEATURE_EXTRACTION_PROMPT = """
You are an expert in requirements analysis and documentation. Below, you will receive the full SRS document along with the project summary. Your task is to:

Thoroughly Analyze the Documents:
- Ensure that no feature or requirement is missed—cover all functional, technical, and non-functional requirements.
- Extract every detail from both the SRS and the project summary, including explicit requirement statements, technical details, and implicit dependencies.

Generate a Comprehensive Final Report:
- Feature-wise Breakdown: List each feature and sub-feature with clear headings.
- Detailed Descriptions: For every feature, provide a detailed description that includes:
  * Exact requirement statements
  * Technical specifications or details mentioned
  * The role and purpose of the feature in the overall project
  * Dependencies and relationships with other features
- Additional Context: Include any other important information or insights you extract from the documents that add clarity or value to the requirements analysis.

Output Flexibility:
- The report can be as long as necessary to ensure completeness.
- Do not summarize or omit any critical information.
"""

# Re-evaluation prompt
RE_EVALUATE_FEATURE_EXTRACTION_PROMPT = """
You are an expert in requirements analysis and documentation. Below, you will receive the original SRS, previous feature extraction report along with user feedback. Your task is to:

Re-Evaluate the Existing Report:
- Carefully analyze the SRS and review the previous feature extraction report alongside the provided user feedback.
- If the feedback indicates that changes or improvements are needed, re-analyze the full SRS document in conjunction with the previous report.
- Ensure that all functional, technical, and non-functional requirements are fully captured.
- Whatever the changes are requested by the user, make it carefully keep in mind that previous extracted feature details should be there. Additionally you have incorporate the changes requested by the user.

Generate an Updated Comprehensive Final Report:
- Feature-wise Breakdown: List each feature and sub-feature with clear, organized headings.
- Detailed Descriptions: For every feature, provide:
  * Exact requirement statements
  * Technical specifications or details mentioned
  * The role and purpose of the feature in the overall project
  * Dependencies and relationships with other features
"""

@router.post("/extract")
async def extract_features(request: FeatureExtractionRequest) -> FeatureResponse:
    try:
        logger.debug("Processing new feature extraction request")

        # Create the prompt message
        prompt = f"{FEATURE_EXTRACTION_PROMPT}\n\nHere is the SRS document content:\n{request.srs_content}\n\nHere is the project summary:\n{request.project_summary}"

        # Generate feature extraction using the prompt
        response = thinking_model.generate_content(prompt)
        
        return FeatureResponse(
            feature_details=response.text,
            status="success"
        )

    except Exception as e:
        logger.error(f"Error in feature extraction: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract features: {str(e)}"
        )

@router.post("/re-evaluate")
async def re_evaluate_features(request: FeatureReEvaluationRequest) -> FeatureResponse:
    try:
        logger.debug("Processing feature re-evaluation request")

        # Create the prompt message
        prompt = f"{RE_EVALUATE_FEATURE_EXTRACTION_PROMPT}\n\nHere is the SRS document content:\n{request.srs_content}\n\nHere is the previous report:\n{request.previous_features}\n\nHere is the user feedback:\n{request.user_feedback}"

        # Generate re-evaluation using the prompt
        response = thinking_model.generate_content(prompt)
        
        return FeatureResponse(
            feature_details=response.text,
            status="success"
        )

    except Exception as e:
        logger.error(f"Error in feature re-evaluation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to re-evaluate features: {str(e)}"
        )