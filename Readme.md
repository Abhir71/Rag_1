# RAG PDF Summarizer
 A local RAG pipeline which summarizes any PDF Docs using ollama, Langchain and Chromadb(DB), all running locallyor privately on your machine without any API.

 # Basic Schema:

 PDF File as imput >> Load & SSPlit into Chunks >> USer Query >> Retrieve relevant Chunks >> Summary output...

 # Prerequisites:

Python 3.9+
Ollama runnig locally
Model(
    Embeeding Model = qwen3-embedding
    output model = mistral
)
