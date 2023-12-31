from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

# Access your environment variables
secret_key = os.getenv('SECRET_KEY')
debug_mode = os.getenv('DEBUG')
db_url = os.getenv('DATABASE_URL')


SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = debug_mode

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = db_url
SQLALCHEMY_TRACK_MODIFICATIONS = False