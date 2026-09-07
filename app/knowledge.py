import os
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


load_dotenv()


PDF_PATH = Path("documents/ResearchPilot_Sample_Knowledge_Base.pdf")
CHROMA_DIR = "chroma_db"


def load_documents():
    reader = PdfReader(PDF_PATH)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": PDF_PATH.name,
                    "page": page_number
                }
            )
        )

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)


def create_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        output_dimensionality=768
    )


def get_vector_store():
    embeddings = create_embeddings()

    vector_store = Chroma(
        collection_name="researchpilot_knowledge",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )

    existing = vector_store.get()

    if not existing["ids"]:
        documents = load_documents()
        chunks = split_documents(documents)

        ids = [f"chunk_{i}" for i in range(len(chunks))]

        vector_store.add_documents(
            documents=chunks,
            ids=ids
        )

        print("Knowledge base indexed.")

    return vector_store


def search_knowledge(query):
    vector_store = get_vector_store()

    results = vector_store.similarity_search(query, k=3)

    output = []

    for result in results:
        output.append(
            f"Source: {result.metadata['source']}\n"
            f"Page: {result.metadata['page']}\n"
            f"Content: {result.page_content}"
        )

    return "\n\n".join(output)


if __name__ == "__main__":
    results = search_knowledge(
        "What is the project code for ResearchPilot?"
    )

    print("\nSearch results:\n")
    print(results)