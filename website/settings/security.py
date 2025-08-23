import os

from dotenv import load_dotenv

# The secret key must be loaded from the environment or a .env file.
load_dotenv(override=False)
SECRET_KEY = os.environ['SECRET_KEY']
