import os
import requests

def download_web_pdf(url: str, key=None, output_path="source.pdf"):
    headers = {}
    if key:
        headers = {"Authorization": f"Bearer {key}"} # use key for authorization if key exists in input
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path
