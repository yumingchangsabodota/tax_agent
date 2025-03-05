
import os
import pdfplumber
import pandas as pd
import csv
import json

from db.mongo.tax_doc_vector_store import vector_store
from ai_model.openai_model import text_embedding_3_small
from db.mongo.tax_doc_vector_store import collection

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


path = "db/migration/tax_pdf"
path_csv = "db/migration/tax_csv"


def extract_tables_from_pdf(filename):
    tables = []
    try:
        with pdfplumber.open(filename) as pdf:
            for page in pdf.pages:
                # Extract table assuming tables with borders
                table = page.extract_table()
                if table:
                    tables.append(table)
        return tables
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return None


def save_tables_as_csv(tables, filename):
    base_filename = filename.split('.')[0]
    for i, table in enumerate(tables):
        header = table[0]
        data = table[3:]
        df = pd.DataFrame(data)
        csv_filename = f"{base_filename}_table_{i+1}.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"Saved table {i+1} as {csv_filename}")


"""
for file in os.listdir(path):
    print(f"Vectorizing {file}")
    file_path = os.path.join(path, file)
    loader = PyPDFLoader(file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000, chunk_overlap=500)
    docs = text_splitter.split_documents(data)
    vector_store.from_documents(
        documents=docs, embedding=text_embedding_3_small, collection=collection)
"""
for file in os.listdir(path):
    print(f"Parsing {file}")
    file_path = os.path.join(path, file)
    csv_path = os.path.join(path_csv, file)
    tables = extract_tables_from_pdf(file_path)
    # print(tables)
    save_tables_as_csv(tables, csv_path)
    break
