
import os

from langchain_openai import OpenAIEmbeddings, ChatOpenAI


COMPLETION_TOKENS = 2000
openai_4o_mini = ChatOpenAI(model="gpt-4o-mini",
                            temperature=0,
                            max_tokens=COMPLETION_TOKENS,
                            streaming=True)


text_embedding_3_small = OpenAIEmbeddings(model="text-embedding-3-small")
