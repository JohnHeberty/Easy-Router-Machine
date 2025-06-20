import os
from dotenv import load_dotenv

load_dotenv()

api_config = {
    "version_api": os.getenv("API_ROUTER_VERSION"),
    "prefix_api": os.getenv("API_PREFIX", "false")
}
