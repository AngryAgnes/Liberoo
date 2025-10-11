from typing import List, Dict
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

class VectorStore:
    def __init__(self, embedding_model: str = "text-embedding-ada-002"):
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def add_texts(self, texts: List[str], metadatas: List[Dict] = None) -> None:
        """Add texts to the vector store"""
        documents = [Document(page_content=text, metadata=meta if meta else {})
                    for text, meta in zip(texts, metadatas or [{}] * len(texts))]
        
        # Split documents into chunks
        split_docs = self.text_splitter.split_documents(documents)
        
        # Create or update vector store
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(split_docs, self.embeddings)
        else:
            self.vector_store.add_documents(split_docs)

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Perform similarity search for the query"""
        if self.vector_store is None:
            raise ValueError("Vector store is empty. Add documents first.")
        
        return self.vector_store.similarity_search(query, k=k)

    def save_local(self, path: str) -> None:
        """Save the vector store locally"""
        if self.vector_store is not None:
            self.vector_store.save_local(path)

    def load_local(self, path: str) -> None:
        """Load the vector store from local storage"""
        self.vector_store = FAISS.load_local(path, self.embeddings)