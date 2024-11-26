import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

load_dotenv("keys")

def collection(name):
    return chromadb.PersistentClient(path="./chroma_data").get_or_create_collection(
        name=name,
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name="text-embedding-ada-002"
        )
    )

if False:
    import llm

    documents = []
    metadatas = []
    ids = []
    id = 10000

    for shoppers in ["men", "women"]:
        instruction = "Yor are a creative catalog writer."
        for product in ["hats", "shirts", "pants", "shoes"]:
            prompt = f"Invent a catlog description (about 200 words) and price for {shoppers}'s {product}. Pure text format, no markdown."
            documents.append(llm.invoke(instruction, prompt))
            metadatas.append({"section": f"{shoppers}'s {product}"})
            ids.append(f"id-{id}")
            id += 1

    def create(name, documents, metadatas, ids):
        collection(name).add(documents=documents, metadatas=metadatas, ids=ids)