import os
from pinecone import Pinecone

def init_pinecone():
    """
    Initialize the Pinecone index with the API key and environment variables.
    
    Returns:
        Index: The initialized Pinecone index.
    """
    PINECONE_INDEX_NAME = "medicalbot"

    pc = Pinecone(
            api_key=os.getenv("PINECONE_API_KEY"),
            region="us-east-1"
        )
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        raise ValueError(f"Index '{PINECONE_INDEX_NAME}' does not exist.")
    return pc.Index(PINECONE_INDEX_NAME)

