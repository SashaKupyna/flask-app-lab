import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-kupyna-lab3")
DEBUG = True
TESTING = False
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
