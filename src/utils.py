import os
from dotenv import load_dotenv

def load_api_key(cli_arg):
    if cli_arg:
        return cli_arg
    load_dotenv()
    return os.getenv("API_KEY")
