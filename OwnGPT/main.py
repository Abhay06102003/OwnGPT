import os
import asyncio
import aiohttp
from googlesearch import search
from bs4 import BeautifulSoup
from ollama import AsyncClient
import torch
# Langchain and vector DB imports
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

class OwnGPT:
    def __init__(self):
        """
        Initialize OwnGPT with Ollama configuration and vector database.
        """
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # print(self.device)
        self.num_results = 2
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        
        # Initialize embeddings and vector store
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        self.vectorstore = Chroma(
            persist_directory="./chroma_db", 
            embedding_function=self.embeddings,
        )
        
        # Text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, 
            chunk_overlap=100
        )

    def get_google_search_urls(self, query):
        """
        Fetch search result URLs from Google.
        """
        try:
            return list(search(query, num_results=self.num_results, lang="en"))
        except Exception as e:
            print(f"Error fetching search results: {e}")
            return []

    async def extract_text_from_url(self, session, url):
        """
        Asynchronously extract and clean text from a single URL.
        """
        try:
            async with session.get(url, headers=self.headers, timeout=10) as response:
                response.raise_for_status()
                content = await response.text()
                
                soup = BeautifulSoup(content, 'html.parser')
                
                # Try multiple methods to extract main content
                article_text = soup.find(['article', 'main', 'div.content', 'div.article-body'])
                
                if article_text:
                    text = article_text.get_text(separator=' ', strip=True)
                else:
                    text = soup.get_text(separator=' ', strip=True)
                
                # Clean up extra whitespaces and remove excessive newlines
                cleaned_text = ' '.join(text.split())
                
                return cleaned_text
        
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return None

    async def extract_and_clean_text(self, urls):
        """
        Asynchronously extract and clean text from multiple URLs.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.extract_text_from_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks)
            
            return dict(zip(urls, results))

    def store_texts_in_vector_db(self, texts):
        """
        Store extracted texts in vector database.
        """
        for url, text in texts.items():
            if text:
                # Split text into chunks
                text_chunks = self.text_splitter.split_text(text)
                
                # Add chunks to vector store with metadata
                self.vectorstore.add_texts(
                    texts=text_chunks, 
                    metadatas=[{'source': url}] * len(text_chunks)
                )

    async def retrieve_relevant_context(self, query, k=3):
        """
        Retrieve relevant context from vector database.
        """
        # Perform similarity search
        results = self.vectorstore.similarity_search(query, k=k)
        
        # Extract and combine context
        context = "\n\n".join([doc.page_content for doc in results])
        return context

    async def generate_response(self, query, context):
        """
        Asynchronously generate a comprehensive response using Ollama.
        """
        # Prepare the prompt with retrieved context
        prompt = f"""
        Context: {context}

        Query: {query}

        Based on the provided context and query, generate a comprehensive and informative response.
        Ensure the response is:
        - Directly relevant to the query
        - Synthesized from the given context
        - Clear and Description Explanatory.
        - Provides valuable insights
        - Summarize and give in detail response in English.
        """

        try:
            async def chat():
                message = {'role': 'user', 'content': prompt}
                async for part in await AsyncClient().chat(model='llama3.2', messages=[message], stream=True):
                    print(part['message']['content'], end='', flush=True)
            await chat()

        except Exception as e:
            print(f"Error communicating with Ollama: {e}")
            return "Sorry, I couldn't generate a response at the moment."

async def main():
    inst = OwnGPT()
    query = "Give me Some news about AI"
    
    # Get search URLs
    print("GETTING URLS")
    urls = inst.get_google_search_urls(query=query)
    print(urls)
    
    # Extract texts from URLs
    print("GETTING TEXTS")
    texts = await inst.extract_and_clean_text(urls)
    
    # Store texts in vector database
    print("STORING TEXTS IN VECTOR DB")
    inst.store_texts_in_vector_db(texts)
    
    # Retrieve relevant context
    print("RETRIEVING RELEVANT CONTEXT")
    context = await inst.retrieve_relevant_context(query)
    # print(context)
    # Generate response
    print("GENERATING RESPONSE")
    response = await inst.generate_response(query=query, context=context)

if __name__ == "__main__":
    asyncio.run(main())