from dotenv import load_dotenv
load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_ollama import OllamaEmbeddings
import os

urls = [
    "https://www.investopedia.com/terms/s/sma.asp",
    "https://www.investopedia.com/terms/e/ema.asp",
    "https://www.investopedia.com/articles/technical/102201.asp",
    "https://lightningchart.com/blog/trader/what-are-keltner-channels/"
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

embedding_model = OllamaEmbeddings(model="nomic-embed-text")

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)

doc_splits = text_splitter.split_documents(docs_list)

#vectorstore = Chroma.from_documents(
#    documents=doc_splits,
#    collection_name="rag-chroma",
#    embedding=embedding_model,
#    persist_directory="./.chroma",
#)

retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    embedding_function=embedding_model,
).as_retriever()

#print("Number of documents:", vectorstore._collection.count())