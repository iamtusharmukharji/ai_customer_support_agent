import os
from dotenv import load_dotenv

load_dotenv()

class Credentials:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.gemini_url = os.getenv('GEMINI_URL')
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.db_schema = os.getenv('DB_SCHEMA_NAME')
        self.db_username = os.getenv('DB_USERNAME')
        self.db_password = os.getenv('DB_PASSWORD')
        self.gemini_model = os.getenv('GEMINI_MODEL')
        self.openai_model = os.getenv('OPENAI_MODEL_CHEAP')



credentials = Credentials()
