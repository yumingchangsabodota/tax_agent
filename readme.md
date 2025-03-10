## Tax Agent

### This is an agent that utilizes augmented retrieval to search for the Taiwan import export tax categories by a given description of a product.

![Example 1](img/example1.png)
![Example 2](img/example2.png)

### Architecture
```mermaid
flowchart LR

user[User Input]
ui[UI - Shiny UI]
api[API - FastAPI]
db_m[(Memory, RAG - MongoDB)]
agent[Agent - Langraph]
llm[LLM Model - OpenAI]

user --> ui --> api --> agent --> llm
llm --> agent --> api --> ui --> user

api --Memory Retrieval--> db_m
db_m --Memory Retrieval--> api
agent --RAG Search--> db_m
db_m --RAG Search--> agent


```


[Tax Category Source](https://fbfh.trade.gov.tw/fh/ap/listCCCf.do)