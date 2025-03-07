

from ai_model.openai_model import text_embedding_3_small

from db.mongo.mongo_connector import mongo_atlas_db
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch

db_name = "tax_doc"
collection_name = "tax_category"
vector_index_name = "tax_category_vector"
collection = mongo_atlas_db[db_name][collection_name]

vector_store = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=text_embedding_3_small,
    index_name=vector_index_name,
    relevance_score_fn="cosine",
)

__all__ = ["vector_store", "collection"]
