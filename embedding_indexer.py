# Builds a vector store from document chunks

from langchain_community.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings  # Or your preferred embedding class

class EmbeddingIndexer:
    def create_vectorstore(self, texts):
        # You may need to provide your own OpenAI key / embedding config here!
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_texts(texts, embedding=embeddings, persist_directory="chroma_db")
        return vectorstore
