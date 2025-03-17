import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
LLAMA_PARSE_API_KEY = os.getenv('LLAMA_PARSE_API_KEY')


# Validate required environment variables
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")
if not LLAMA_PARSE_API_KEY:
    raise ValueError("LLAMA_PARSE_API_KEY not found in environment variables")
