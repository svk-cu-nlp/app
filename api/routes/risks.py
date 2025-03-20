from fastapi import APIRouter, HTTPException
import google.generativeai as genai
import os
import logging
from ..models import RiskAnalysisRequest, RiskAnalysisResponse

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Note: The prefix should match what your frontend is calling
router = APIRouter(prefix="/api/risks", tags=["Risks"])

# Initialize Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

# Risk analysis prompt from codebase_for_apis.ipynb
RISK_ANALYSIS_PROMPT = """
You are an expert in risk analysis and security assessment for software requirements specifications (SRS). You will be provided with an SRS document along with detailed feature descriptions.

Your task is to systematically analyze each feature and requirement, ensuring that no aspect is overlooked. Follow these steps:

Identify Possible Risks:
- Evaluate each feature's implementation and operation.
- Consider risks such as system failures, incorrect functionality, regulatory compliance issues, and operational inefficiencies.

Analyze Potential Vulnerabilities and Security Issues:
- Identify any weaknesses that may be exploited.
- Consider attack vectors such as unauthorized access, data breaches, injection attacks, or denial-of-service vulnerabilities.
- Highlight compliance risks with standards like ISO 27001, GDPR, or HIPAA if applicable.

Provide Risk Mitigation and Security Guidelines:
- Suggest industry best practices to reduce risks.
- Recommend tools, frameworks, or processes to enhance security and compliance.
- Provide step-by-step strategies for preventing vulnerabilities from being exploited.

Ensure that your analysis covers every feature and requirement within the document without omissions. Present your findings in a structured manner, clearly linking risks to mitigation strategies.
"""

@router.post("/analyze")
async def analyze_risks(request: RiskAnalysisRequest) -> RiskAnalysisResponse:
    try:
        logger.debug("Processing risk analysis request")
        logger.debug(f"Received features: {request.features[:100]}...")  # Log first 100 chars

        # Create the prompt message
        prompt = f"{RISK_ANALYSIS_PROMPT}\n\nHere is the SRS document content:\n{request.srs_content}\n\nHere are the feature details:\n{request.features}"

        # Generate risk analysis using the prompt
        response = model.generate_content(prompt)
        
        logger.debug("Successfully generated risk analysis")
        return RiskAnalysisResponse(
            risk_analysis=response.text,
            status="success"
        )

    except Exception as e:
        logger.error(f"Error in risk analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze risks: {str(e)}"
        )
