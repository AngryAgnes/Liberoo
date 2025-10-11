from typing import List, Dict, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from .vector_store import VectorStore

class RAGModel:
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        embedding_model: str = "text-embedding-ada-002"
    ):
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.vector_store = VectorStore(embedding_model=embedding_model)
        
        # Default prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful travel assistant. Use the following context to answer the question.\n\nContext: {context}"),
            ("human", "{question}")
        ])

    def add_knowledge(self, texts: List[str], metadatas: Optional[List[Dict]] = None) -> None:
        """Add knowledge to the RAG system"""
        self.vector_store.add_texts(texts, metadatas)

    def _format_context(self, docs: List[Document]) -> str:
        """Format retrieved documents into context string"""
        return "\n\n".join([doc.page_content for doc in docs])

    async def generate_response(
        self,
        question: str,
        num_contexts: int = 4,
        custom_prompt_template: Optional[ChatPromptTemplate] = None
    ) -> str:
        """Generate a response using RAG"""
        # Retrieve relevant documents
        relevant_docs = self.vector_store.similarity_search(question, k=num_contexts)
        context = self._format_context(relevant_docs)

        # Use custom prompt template if provided
        prompt = custom_prompt_template or self.prompt_template
        
        # Generate response
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "context": context,
            "question": question
        })
        
        return response.content

    def save_knowledge_base(self, path: str) -> None:
        """Save the vector store to disk"""
        self.vector_store.save_local(path)

    def load_knowledge_base(self, path: str) -> None:
        """Load the vector store from disk"""
        self.vector_store.load_local(path)

    def set_prompt_template(self, prompt_template: ChatPromptTemplate) -> None:
        """Update the prompt template"""
        self.prompt_template = prompt_template