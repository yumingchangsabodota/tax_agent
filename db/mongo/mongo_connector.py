import os

from pymongo import MongoClient

MONGO_ATLAS_HOST = os.getenv(
    "MONGO_ATLAS_HOST", "localhost")
MONGO_ATLAS_USER = os.getenv(
    "MONGO_ATLAS_USER")
MONGO_ATLAS_PASSWORD = os.getenv(
    "MONGO_ATLAS_PASSWORD")

MONGO_ATLAS_CONNECTION_STRING = f"mongodb+srv://{MONGO_ATLAS_USER}:{MONGO_ATLAS_PASSWORD}@{MONGO_ATLAS_HOST}/"

mongo_atlas_db = MongoClient(MONGO_ATLAS_CONNECTION_STRING)

__all__ = ["mongo_atlas_db"]
