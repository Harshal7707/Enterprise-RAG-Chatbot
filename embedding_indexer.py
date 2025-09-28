
from langchain_community.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings  

class EmbeddingIndexer:
    def create_vectorstore(self, texts):
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_texts(texts, embedding=embeddings, persist_directory="chroma_db")
        return vectorstore
