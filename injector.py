from config.log_config import create_log
from dotenv import load_dotenv


''' pip install python-dotenv'''
load_dotenv() # will search for .env file in local folder and load variables 
    
# Initialize & Inject with only one instance
logger = create_log()
