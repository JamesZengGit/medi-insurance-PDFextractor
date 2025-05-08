import os
import requests
import logging

logger = logging.getLogger(__name__)

def download_web_pdf(url: str, key=None, output_path="source.pdf"):
    headers = {}
    if key:
        headers = {"Authorization": f"Bearer {key}"} # use key for authorization if key exists in input
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    return None
