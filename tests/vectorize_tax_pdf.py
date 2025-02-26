
import os

from db.mongo.tax_doc_vector_store import vector_store
from ai_model.openai_model import text_embedding_3_small
from db.mongo.tax_doc_vector_store import collection

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


path = "tax_pdf"

for file in os.listdir(path):
    file_path = os.path.join(path, file)
    loader = PyPDFLoader(file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=500)
    docs = text_splitter.split_documents(data)
    vector_store.from_documents(
        documents=docs, embedding=text_embedding_3_small, collection=collection)
