import os

from dotenv import load_dotenv

load_dotenv(override=False)

# The secret key must be loaded from the environment or a .env file.
SECRET_KEY = os.environ['SECRET_KEY']
