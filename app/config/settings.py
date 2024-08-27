import os
import logging
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(level=logging.INFO)

os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
os.environ["AZURE_OPENAI_API_VERSION"] = os.getenv("AZURE_OPENAI_API_VERSION")


logging.info("Environment variables for Azure OpenAI API set.")

try:
    model = AzureChatOpenAI(
        deployment_name="gpt-4o",
        model_name="gpt-4o",
        openai_api_type="azure",
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    )
    logging.info("Model initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing model: {e}")
    exit()
