from unittest.mock import patch, MagicMock
from src.main import load_and_split_pdf, build_vector_db, build_rag_chain, summarize_pdf

@patch("src.main.PyPDFLoader")
def test_load_and_split_pdf(mock_loader_class):
    """PDF is loaded and split into chunks."""
    mock_doc = MagicMock()
    mock_doc.page_content = "This is a test sentence. " * 50  
    mock_doc.metadata = {"source": "fake.pdf"}

    mock_loader_class.return_value.load.return_value = [mock_doc]

    chunks = load_and_split_pdf("fake.pdf", chunk_size=100, chunk_overlap=10)

    assert isinstance(chunks, list)
    assert len(chunks) > 0

@patch("src.main.OllamaEmbeddings")
@patch("src.main.Chroma")
def test_build_vector_db(mock_chroma, mock_embeddings):
    """Vector DB is created from document chunks."""
    mock_texts = [MagicMock(), MagicMock()]
    mock_chroma.from_documents.return_value = MagicMock()

    db = build_vector_db(mock_texts)

    mock_chroma.from_documents.assert_called_once()
    assert db is not None

@patch("src.main.ChatOllama")
def test_build_rag_chain(mock_ollama):
    """RAG chain is built without errors."""
    mock_vector_db = MagicMock()
    mock_vector_db.as_retriever.return_value = MagicMock()

    chain = build_rag_chain(mock_vector_db, llm_model="mistral")

    assert chain is not None
    mock_ollama.assert_called_once_with(model="mistral")

@patch("src.main.build_rag_chain")
@patch("src.main.build_vector_db")
@patch("src.main.load_and_split_pdf")
def test_summarize_pdf(mock_split, mock_db, mock_chain):
    """End-to-end summarize_pdf returns a string."""
    mock_split.return_value = [MagicMock()]
    mock_db.return_value = MagicMock()

    # Simulate chain.invoke() returning a summary string
    mock_chain_instance = MagicMock()
    mock_chain_instance.invoke.return_value = "This PDF is about machine learning."
    mock_chain.return_value = mock_chain_instance

    result = summarize_pdf("fake.pdf")

    assert isinstance(result, str)
    assert len(result) > 0
    mock_split.assert_called_once_with("fake.pdf")