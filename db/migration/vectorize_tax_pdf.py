
import os
import pdfplumber
from uuid import uuid4

from typing import List
from langchain_core.documents import Document

from pydantic import BaseModel, Field
from db.mongo.tax_doc_vector_store import vector_store
from ai_model.openai_model import text_embedding_3_small
from db.mongo.tax_doc_vector_store import collection


path = "db/migration/tax_pdf"


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


def set_empty_cell(row):
    for i, cell in enumerate(row):
        if cell == "":
            row[i] = " "
    return row


def parse_tables_to_markdown(tables) -> List[str]:
    markdowns = []
    columns = ["稅則號別", "貨品分類列號 CCC Code", "檢查號碼 CD",
               "貨名 Description of goods", "輸入規定 Import", "輸出規定 Export"]

    headers = "|"+"|".join(columns)+"|"+"\n"
    headers += "|"+"|".join([":---------------:"]*len(columns))+"|"+"\n"
    for i, table in enumerate(tables):
        markdown = headers
        table_rows = table[2:]
        for row in table_rows:
            row = [str(cell).replace("\n", '') for cell in row]
            row = set_empty_cell(row)
            markdown += "|"+"|".join(row)+"|"+"\n"
        markdowns.append(markdown)
    return markdowns


def insert_documents(docs: List[str]):
    pages = [Document(page_content=doc)
             for doc in docs]
    ids = [str(uuid4()) for _ in range(len(pages))]
    vector_store.add_documents(documents=pages, doc_ids=ids)


for file in os.listdir(path):
    print(f"Parsing {file}")
    file_path = os.path.join(path, file)
    tables = extract_tables_from_pdf(file_path)
    makrdowns = parse_tables_to_markdown(tables)
    insert_documents(makrdowns)
    print(f"Done parsing {file}")
