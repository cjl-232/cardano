import os

from dotenv import load_dotenv

load_dotenv(override=False)

# Debug mode should be disabled unless specified in the environment.
DEBUG = os.environ.get('DEBUG', 'False').upper() == 'TRUE'
