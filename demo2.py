import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
import config
import rag_components
from db.weaviateDB import connect_to_weaviate
from utils.AdvancedLawRetriever import AdvancedLawRetriever
from services.reranker_service import get_reranker_compressor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from prompt_templete import UNIFIED_PREPROCESSING_PROMPT
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global objects for reuse
embeddings = None
weaviate_client = None
llm = None
reranker = None
retriever = None
qa_chain = None
preprocessing_chain = None
executor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Replace startup/shutdown events with lifespan context manager."""
    global embeddings, weaviate_client, llm, reranker, retriever, qa_chain, preprocessing_chain, executor

    # Startup
    logger.info("Starting RAG API initialization...")
    executor = ThreadPoolExecutor(max_workers=4)

    logger.info("Loading embedding model...")
    embeddings = rag_components.get_huggingface_embeddings(config.EMBEDDING_MODEL_NAME, device="cpu")
    if not embeddings:
        raise RuntimeError("Failed to load embedding model.")

    logger.info("Connecting to Weaviate...")
    weaviate_client = connect_to_weaviate(run_diagnostics=False)
    if not weaviate_client:
        raise RuntimeError("Failed to connect to Weaviate.")

    logger.info("Loading LLM...")
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if hasattr(rag_components, 'get_google_llm') and google_api_key:
        llm = rag_components.get_google_llm(google_api_key)
    if not llm:
        raise RuntimeError("Failed to load LLM. Please set GOOGLE_API_KEY.")

    logger.info("Loading reranker...")
    reranker = get_reranker_compressor()
    if not reranker:
        raise RuntimeError("Failed to load reranker.")

    logger.info("Setting up retriever...")
    retriever = AdvancedLawRetriever(
        client=weaviate_client,
        collection_name=config.WEAVIATE_COLLECTION_NAME,
        llm=llm,
        reranker=reranker,
        embeddings_model=embeddings
    )

    logger.info("Building RAG chain...")
    qa_chain = rag_components.create_qa_chain(
        llm=llm,
        retriever=retriever,
        process_input_llm=llm
    )

    logger.info("Building preprocessing chain...")
    preprocessing_prompt = ChatPromptTemplate.from_template(UNIFIED_PREPROCESSING_PROMPT)
    parser = JsonOutputParser()
    preprocessing_chain = preprocessing_prompt | llm | parser

    logger.info("RAG API initialization completed successfully!")
    yield  # Application runs here

    # Shutdown
    logger.info("Shutting down executor...")
    if executor:
        executor.shutdown(wait=True)
    logger.info("Shutdown complete.")


app = FastAPI(title="LexiBot RAG API", lifespan=lifespan)


class RAGQueryRequest(BaseModel):
    question: str
    chat_history: Optional[List[Any]] = []


class RAGQueryResponse(BaseModel):
    classification: str
    rewritten_question: str
    answer: str
    sources: Optional[List[Any]] = None


def run_preprocessing(question: str, chat_history: List[Any]):
    """Run preprocessing in separate thread"""
    try:
        return preprocessing_chain.invoke({"input": question, "chat_history": chat_history})
    except Exception as e:
        logger.warning(f"Preprocessing failed: {e}, using fallback")
        return {"classification": "unknown", "rewritten_question": question}


def run_rag_pipeline(question: str, chat_history: List[Any]):
    """Run RAG pipeline in separate thread"""
    input_data = {"input": question, "chat_history": chat_history}
    return qa_chain.invoke(input_data)


def format_sources_optimized(sources):
    """Optimized source formatting"""
    if not sources:
        return None

    formatted_sources = []
    for doc in sources:
        content = doc.page_content
        preview = content[:200]
        if len(content) > 200:
            preview += "..."

        formatted_sources.append({
            "source": doc.metadata.get("source", "[No source]"),
            "preview": preview
        })

    return formatted_sources


@app.post("/rag/query", response_model=RAGQueryResponse)
async def rag_query(request: RAGQueryRequest):
    global qa_chain, preprocessing_chain, executor

    if not qa_chain or not preprocessing_chain:
        raise HTTPException(status_code=500, detail="RAG pipeline not initialized.")

    try:
        chat_history = request.chat_history or []
        loop = asyncio.get_event_loop()

        preprocessing_future = loop.run_in_executor(
            executor, run_preprocessing, request.question, chat_history
        )
        rag_future = loop.run_in_executor(
            executor, run_rag_pipeline, request.question, chat_history
        )

        preprocessing_result, rag_result = await asyncio.gather(
            preprocessing_future, rag_future, return_exceptions=True
        )

        if isinstance(preprocessing_result, Exception):
            logger.warning(f"Preprocessing failed: {preprocessing_result}")
            classification = "unknown"
            rewritten_question = request.question
        else:
            classification = preprocessing_result.get("classification", "unknown")
            rewritten_question = preprocessing_result.get("rewritten_question", request.question)

        if isinstance(rag_result, Exception):
            raise HTTPException(status_code=500, detail=f"RAG pipeline failed: {rag_result}")

        if isinstance(rag_result, dict):
            answer = rag_result.get("answer", str(rag_result))
            sources = rag_result.get("context")
        else:
            answer = str(rag_result)
            sources = None

        formatted_sources = format_sources_optimized(sources)

        return RAGQueryResponse(
            classification=classification,
            rewritten_question=rewritten_question,
            answer=answer,
            sources=formatted_sources
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in RAG pipeline: {e}")
        raise HTTPException(status_code=500, detail=f"Error during RAG pipeline: {e}")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "components": {
            "llm": llm is not None,
            "retriever": retriever is not None,
            "qa_chain": qa_chain is not None,
            "preprocessing_chain": preprocessing_chain is not None
        }
    }


@app.post("/warmup")
async def warmup():
    try:
        test_query = "Luật giao thông"
        test_request = RAGQueryRequest(question=test_query, chat_history=[])
        await rag_query(test_request)
        return {"status": "warmed up successfully"}
    except Exception as e:
        logger.warning(f"Warmup failed: {e}")
        return {"status": "warmup completed with warnings", "warning": str(e)}
