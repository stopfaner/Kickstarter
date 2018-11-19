import os


DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_PORT = os.environ.get("DATABASE_PORT", 5432)

DATABASE_USER = "user"
DATABASE_PASSWORD = "password"
DATABASE_NAME = "kickstarter"
