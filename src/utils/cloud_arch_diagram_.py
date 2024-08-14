import requests
import os
import uuid
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_cloud_architecture_diagram(feature_name, additional_context=""):
    api_key = os.getenv("ERASER_IO_API_KEY")
    if api_key is None:
        logger.error("ERASER_IO_API_KEY environment variable is not set")
        raise ValueError("ERASER_IO_API_KEY environment variable is not set")

    url = "https://app.eraser.io/api/render/prompt"

    text_body = f"""
    Create a cloud architecture diagram for the feature: {feature_name}
    Additional context: {additional_context}
    Include main components, their interactions, and any cloud services involved.
    """

    payload = {
        "text": text_body,
        "diagramType": "cloud-architecture-diagram",
        "background": True,
        "theme": "light",
        "scale": "3",
        "returnFile": True
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    try:
        logger.info("Sending request to generate cloud architecture diagram.")
        response = requests.post(url, json=payload, headers=headers)
        
        # Log the status code
        logger.info(f"Received response with status code: {response.status_code}")
        response.raise_for_status()

        output_dir = os.path.join("output", "cloud-architecture-diagram")
        os.makedirs(output_dir, exist_ok=True)

        random_file_name = f"cloud_arch_diagram_{uuid.uuid4().hex}.png"
        output_path = os.path.join(output_dir, random_file_name)

        with open(output_path, "wb") as f:
            f.write(response.content)

        logger.info(f"Cloud architecture diagram generated successfully at: {output_path}")
        return output_path
    except requests.RequestException as e:
        logger.error(f"Error making request: {e}")
        raise Exception(f"Error generating cloud architecture diagram: {str(e)}")
    except IOError as e:
        logger.error(f"Error saving file: {e}")
        raise Exception(f"Error saving cloud architecture diagram: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise Exception(f"Error generating cloud architecture diagram: {str(e)}")