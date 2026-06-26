from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
#Retrieval and shit
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaEmbeddings, ChatOllama



#pdf file loader

# file_path = "/Users/abhisheksingh/Documents/CV/Abhishek_Singh_CV.pdf"


# /Users/abhisheksingh/Documents/CV/Abhishek_Singh_.pdf


# docs[10]

#now split the shit into chunks
def load_and_split_pdf(file_path: str, chunk_size: int = 500, chunk_overlap: int = 50):
    """Load pdf and split shit into chunks"""
    loader = PyPDFLoader(file_path)
    docs=loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(docs)


def build_vector_db(texts, embedding_model: str = "qwen3-embedding", collection_name: str = "local_rag"):  ## Chroma.from_documents(
    """create a vector chroma db and store chunk data."""
    return Chroma.from_documents(
        documents=texts,
        embedding=OllamaEmbeddings(model=embedding_model),
        collection_name=collection_name
    )

def build_rag_chain(vector_db, llm_model: str= "mistral"):
    """Build the RAG CHain from vector db and llm."""
    llm=ChatOllama(model=llm_model)
    retriever= vector_db.as_retriever()

    template = """You are an expert at reformulating search queries to maximize document retrieval accuracy.
     - Answer the User Question in Simple Manner.
     Answer the question based ONLY on the following context:
{context}
Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

def summarize_pdf(file_path: str, question: str = "Who is the candidate in the document??") -> str:
    """End-to-end: load PDF, build RAG chain, return answer."""
    texts = load_and_split_pdf(file_path)
    vector_db = build_vector_db(texts)
    chain = build_rag_chain(vector_db)
    return chain.invoke(question)
    # print(return)

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "/Users/abhisheksingh/Documents/CV/Abhishek_Singh_CV.pdf"
    print(summarize_pdf(path))


# local_model="mistral"


# QUERY_PROMPT = PromptTemplate(
#     input_variables=["question"],
#     template="""You are an AI language model assistant. Your task is to generate
#     different versions of the given user question and retrieve relevant documents 
#     information from a vector database. By generating multiple perspectives on the 
#     user question, your goal is to help the user overcome some of the limitations 
#     of the distance-based similarity search. Provide these alternative questions separated by newlines.
#     Original question: {question}""",
# )

# retriever = vector_db.as_retriever()


# template = """Answer the question based ONLY on the following context:
# {context}
# Question: {question}
# """

# prompt = ChatPromptTemplate.from_template(template)

# chain = (
#     {"context":retriever, "question":RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# response = chain.invoke("What is this pdf about? Can you give me summary in point?")

# print(response)