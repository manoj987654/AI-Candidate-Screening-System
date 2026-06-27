from typing import List, Optional
import os
import logging

logger = logging.getLogger(__name__)

# Try to import ML packages, handle gracefully if unavailable
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    logger.warning("sentence_transformers not available - semantic search disabled")
    HAS_SENTENCE_TRANSFORMERS = False
    SentenceTransformer = None

try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMADB = True
except ImportError:
    logger.warning("chromadb not available - vector database disabled")
    HAS_CHROMADB = False
    chromadb = None
    Settings = None


class RAGService:
    """Service for Retrieval-Augmented Generation pipeline"""
    
    def __init__(self, vector_db_path: str = "./vector_db"):
        """
        Initialize RAG service with vector database
        
        Args:
            vector_db_path: Path to store vector database
        """
        self.vector_db_path = vector_db_path
        self.embedding_model = None
        self.client = None
        self.collections = {}
        
        logger.info(f"Initializing RAGService with path: {vector_db_path}")
        
        # Check if ML packages are available
        if not HAS_SENTENCE_TRANSFORMERS or not HAS_CHROMADB:
            logger.warning("ML packages not fully available - running in degraded mode")
            logger.info("System will operate without semantic search capabilities")
            return
        
        try:
            # Initialize embedding model
            logger.info("Loading Sentence Transformer model...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✓ Embedding model loaded successfully")
            
            # Initialize Chroma client
            os.makedirs(vector_db_path, exist_ok=True)
            settings = Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=vector_db_path,
                anonymized_telemetry=False
            )
            self.client = chromadb.Client(settings)
            logger.info("✓ ChromaDB client initialized")
            
            logger.info("RAGService initialization complete")
        except Exception as e:
            logger.error(f"Failed to initialize RAGService: {str(e)}")
            self.embedding_model = None
            self.client = None
    
    def ingest_knowledge(
        self,
        role: str,
        documents: List[str],
        metadata: Optional[List[dict]] = None
    ) -> None:
        """
        Ingest documents into the knowledge base
        
        Args:
            role: Target role (e.g., 'ml-engineer', 'backend-engineer')
            documents: List of text chunks to ingest
            metadata: Optional metadata for each document
            
        Raises:
            ValueError: If ingestion fails
        """
        if not documents:
            raise ValueError("No documents provided for ingestion")
        
        # Check if ML packages are available
        if not self.client or not self.embedding_model:
            logger.warning(f"Cannot ingest knowledge for {role} - ML packages not available")
            logger.info("Knowledge ingestion skipped in degraded mode")
            return
        
        collection_name = f"knowledge_{role.lower().replace(' ', '_')}"
        
        try:
            logger.info(f"Starting knowledge ingestion for role: {role}")
            logger.debug(f"Collection name: {collection_name}, Documents: {len(documents)}")
            
            # Delete existing collection if it exists
            try:
                self.client.delete_collection(name=collection_name)
                logger.debug(f"Deleted existing collection: {collection_name}")
            except Exception as e:
                logger.debug(f"No existing collection to delete: {str(e)}")
            
            # Create new collection
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.debug(f"Created collection: {collection_name}")
            
            # Generate embeddings and add to collection
            logger.info(f"Generating embeddings for {len(documents)} documents...")
            embeddings = self.embedding_model.encode(documents)
            logger.debug(f"Generated embeddings shape: {embeddings.shape}")
            
            # Prepare data for insertion
            ids = [f"doc_{i}" for i in range(len(documents))]
            metadatas = metadata or [{"role": role} for _ in documents]
            
            collection.add(
                ids=ids,
                embeddings=embeddings.tolist(),
                documents=documents,
                metadatas=metadatas
            )
            
            self.collections[role] = collection
            logger.info(f"✓ Successfully ingested {len(documents)} documents for role: {role}")
            
        except Exception as e:
            logger.error(f"Failed to ingest knowledge for role {role}: {str(e)}")
            raise ValueError(f"Failed to ingest knowledge for role {role}: {str(e)}")
    
    def retrieve_context(
        self,
        role: str,
        query: str,
        top_k: int = 3
    ) -> List[str]:
        """
        Retrieve relevant context from knowledge base
        
        Args:
            role: Target role
            query: Query string
            top_k: Number of top results to retrieve
            
        Returns:
            List of relevant context chunks
        """
        # Check if ML packages are available
        if not self.client or not self.embedding_model:
            logger.warning("Cannot retrieve context - ML packages not available")
            return []
        
        collection_name = f"knowledge_{role.lower().replace(' ', '_')}"
        
        try:
            if not query.strip():
                logger.warning("Empty query provided for retrieval")
                return []
            
            logger.debug(f"Retrieving context for role: {role}, query: {query[:50]}...")
            
            collection = self.client.get_collection(name=collection_name)
            
            results = collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            # Extract documents from results
            if results and results['documents']:
                retrieved = results['documents'][0]
                logger.debug(f"Retrieved {len(retrieved)} context chunks")
                return retrieved
            
            logger.warning(f"No results retrieved for query: {query[:50]}...")
            return []
            
        except Exception as e:
            logger.error(f"Error retrieving context for role {role}: {str(e)}")
            return []
    
    def construct_retrieval_queries(
        self,
        resume_data: dict,
        role: str
    ) -> List[str]:
        """
        Construct queries based on resume and role
        
        Args:
            resume_data: Extracted resume information
            role: Target job role
            
        Returns:
            List of query strings for retrieval
        """
        queries = []
        
        try:
            # Query based on skills
            skills = resume_data.get('skills', [])
            if skills:
                skills_str = ", ".join(skills[:3])
                queries.append(f"{role} skills required for {skills_str}")
            
            # Query based on role
            queries.append(f"Core concepts and principles for {role}")
            
            # Query based on technologies
            technologies = resume_data.get('technologies', [])
            if technologies:
                tech_str = ", ".join(technologies[:2])
                queries.append(f"Best practices using {tech_str}")
            
            # Query based on domain
            domains = resume_data.get('domain_exposure', [])
            if domains:
                domain = domains[0]
                queries.append(f"{role} in {domain} domain")
            
            # Add default queries if needed
            if not queries:
                queries = [f"Fundamental concepts for {role}"]
            
            logger.debug(f"Constructed {len(queries)} retrieval queries: {queries[:2]}...")
            return queries
            
        except Exception as e:
            logger.error(f"Error constructing retrieval queries: {str(e)}")
            return [f"Fundamental concepts for {role}"]
    
    def check_collection_exists(self, role: str) -> bool:
        """
        Check if knowledge collection exists for a role
        
        Args:
            role: Target role
            
        Returns:
            True if collection exists, False otherwise
        """
        collection_name = f"knowledge_{role.lower().replace(' ', '_')}"
        
        try:
            self.client.get_collection(name=collection_name)
            return True
        except:
            return False
    
    def get_collection_stats(self, role: str) -> dict:
        """
        Get statistics about a knowledge collection
        
        Args:
            role: Target role
            
        Returns:
            Dictionary with collection statistics
        """
        collection_name = f"knowledge_{role.lower().replace(' ', '_')}"
        
        try:
            collection = self.client.get_collection(name=collection_name)
            count = collection.count()
            return {
                "role": role,
                "collection_name": collection_name,
                "document_count": count,
                "status": "active"
            }
        except Exception as e:
            logger.warning(f"Could not get stats for {role}: {str(e)}")
            return {
                "role": role,
                "collection_name": collection_name,
                "status": "not_found"
            }
