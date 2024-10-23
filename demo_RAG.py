import os
from rufus import RufusClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import TokenTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import openai

def main():
    """
    This script implements a simple RAG (Retrieval-Augmented Generation) system using LangChain and OpenAI.
    It crawls a specified URL to scrape content, processes it into manageable chunks, embeds the text for retrieval, 
    and sets up a QA chain to answer queries by retrieving relevant documents from the vector store.

    Steps:
    1. Crawl a webpage for content.
    2. Process and split the content into chunks.
    3. Embed the chunks and store them in a FAISS vector store.
    4. Set up a question-answering system (RAG) using a ChatOpenAI LLM.
    5. Query the QA system and retrieve the results.

    This script demonstrates how to use LangChain's OpenAI API integration and document retrieval functionalities to 
    build a simple RAG system.
    """

    # Initialize Rufus client
    client = RufusClient(api_key=os.getenv('OPENAI_API_KEY'))

    # Step 1: Rufus Crawling
    url = "https://www.bu.edu/cs/masters/program/"
    instructions = "Find information about different programs and admission FAQs."
    documents = client.scrape(url=url, instructions=instructions, max_depth=3)

    # Extract content from documents
    text_data = []
    for doc in documents:
        content = doc.get('content', '')
        if isinstance(content, str) and content.strip():
            text_data.append(content.strip())
        elif isinstance(content, list):
            joined_content = " ".join(
                [str(item).strip() for item in content if isinstance(item, str) and item.strip()]
            )
            if joined_content:
                text_data.append(joined_content)

    # Combine all content into a single string
    combined_text = "\n".join(text_data)

    # Step 2: Split the text into chunks
    text_splitter = TokenTextSplitter(chunk_size=300, chunk_overlap=50)
    texts = text_splitter.split_text(combined_text)

    # Step 3: Create embeddings and store in vector store
    embeddings = OpenAIEmbeddings()
    faiss_store = FAISS.from_texts(texts, embeddings)

    # Step 4: Create a RetrievalQA chain
    llm = ChatOpenAI(temperature=0)
    retriever = faiss_store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )

    # Query the QA chain
    query = "What are the main programs under Boston University CS department?"

    # Step 5: Retrieve Relevant Documents and Answer the Query
    try:
        result = qa_chain.invoke({"query": query})
        answer = result['result']
        source_docs = result['source_documents']

        # Output the answer and sources
        print("\nAnswer:", answer)
    except openai.OpenAIError as e:
        print(f"OpenAI API Error: {e}")

# Run the main function
if __name__ == "__main__":
    main()