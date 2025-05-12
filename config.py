from dotenv import load_dotenv
import os

load_dotenv(".secrets/.env")


class Environment:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    TENANT_ID = os.getenv("TENANT_ID")
    SCOPE = os.getenv("SCOPE")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    STATE = os.getenv("STATE")
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    AUTHORIZE_URL = f"{AUTHORITY}/oauth2/v2.0/authorize"
    TOKEN_URL = f"{AUTHORITY}/oauth2/v2.0/token"