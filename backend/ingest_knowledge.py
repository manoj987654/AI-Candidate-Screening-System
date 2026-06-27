"""
Knowledge base initialization and ingestion script

This script ingests role-specific knowledge into the vector database (ChromaDB).
Run this once before starting the application.

Usage:
    python ingest_knowledge.py
"""
import sys
import logging

# Add current directory to path
sys.path.insert(0, '.')

from app.services import RAGService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def ingest_ml_knowledge():
    """Ingest ML-specific knowledge base"""
    
    logger.info("=" * 80)
    logger.info("INGESTING ML ENGINEER KNOWLEDGE BASE")
    logger.info("=" * 80)
    
    rag_service = RAGService()
    
    # Sample knowledge chunks for ML role
    ml_knowledge = [
        """Machine Learning Fundamentals:
Supervised learning involves training a model using labeled data where the target output is known. 
The model learns to map input features to output labels. Common algorithms include linear regression for 
continuous outputs, logistic regression for binary classification, decision trees for non-linear patterns, 
and support vector machines for high-dimensional classification. The key challenges in supervised learning 
include data quality, feature representation, and generalization to unseen data.""",
        
        """Unsupervised Learning and Clustering:
Unsupervised learning discovers patterns in unlabeled data. Clustering algorithms like K-means partition 
data into groups based on similarity. Hierarchical clustering creates tree-based cluster hierarchies. 
DBSCAN finds density-based clusters. Dimensionality reduction techniques like Principal Component Analysis (PCA) 
identify the most important features and reduce computational complexity. These techniques help with data exploration, 
visualization, and preprocessing.""",
        
        """Feature Engineering Best Practices:
Feature engineering is creating meaningful features from raw data that improve model performance. 
Techniques include normalization (scaling to 0-1), standardization (mean=0, std=1), one-hot encoding for 
categorical variables, and interaction features combining multiple variables. Domain knowledge is crucial for 
identifying relevant features. Feature selection methods like mutual information and correlation analysis help 
remove redundant features. Poor features result in poor models regardless of algorithm complexity.""",
        
        """Preventing Overfitting:
Overfitting occurs when a model memorizes training data including noise and fails to generalize to new data. 
Signs include high training accuracy but poor test accuracy. Prevention techniques:
- Use train/validation/test split to assess generalization
- Apply regularization (L1/Lasso for feature selection, L2/Ridge for weight constraint)
- Use ensemble methods like Random Forests and Gradient Boosting
- Perform cross-validation with multiple fold splits
- Reduce model complexity (fewer parameters, shallower trees)
- Collect more training data to reduce noise impact
Early stopping in neural networks prevents training too long.""",
        
        """Model Evaluation Metrics:
Classification metrics: Accuracy (correct predictions), Precision (true positives / predicted positives), 
Recall (true positives / actual positives), F1-score (harmonic mean of precision and recall). 
Regression metrics: Mean Squared Error (MSE) for penalizing large errors, Root Mean Squared Error (RMSE) in 
original units, Mean Absolute Error (MAE) for interpretability. Confusion matrix shows true/false positives/negatives. 
ROC curve plots true positive rate vs false positive rate. AUC measures classifier discrimination ability. 
Different metrics suit different problems - prioritize recall for rare diseases, precision for spam detection.""",
        
        """Neural Networks and Deep Learning:
Neural networks consist of input, hidden, and output layers of interconnected neurons. Each neuron computes 
weighted sum of inputs plus bias through an activation function. Activation functions introduce non-linearity:
- ReLU (Rectified Linear Unit): max(0, x) - most popular for hidden layers
- Sigmoid: 1/(1+e^-x) - used for binary classification output
- Tanh: hyperbolic tangent - similar to sigmoid but output range [-1,1]
- Softmax: for multi-class classification output
Deep neural networks stack multiple layers to learn hierarchical representations. Backpropagation computes gradients 
and updates weights. Batch normalization, dropout, and regularization prevent overfitting.""",
        
        """Natural Language Processing (NLP):
NLP involves processing text data for language understanding. Tokenization splits text into words/subwords. 
Stemming and lemmatization reduce words to root forms. Word embeddings represent words as vectors:
- Word2Vec: Continuous Bag of Words (CBOW) or Skip-gram predict context from word or vice versa
- GloVe: Global Vectors combine global matrix factorization with local context windows
- FastText: Includes subword information for better handling of rare words
Transformer models like BERT and GPT use attention mechanisms to capture long-range dependencies. 
Common tasks: sentiment analysis, named entity recognition, machine translation, question answering.""",
        
        """Optimization and Gradient Descent:
Gradient descent iteratively updates model parameters to minimize loss function. The gradient points direction 
of steepest increase, so negative gradient points toward minimum. Learning rate controls step size - too high causes 
oscillation, too low causes slow convergence. Variants:
- Batch Gradient Descent: uses entire dataset
- Stochastic GD (SGD): uses single sample - noisier but faster
- Mini-batch SGD: compromise using small batches
- Momentum: accelerates gradient in consistent direction
- Adam: combines momentum with per-parameter adaptive learning rates
- RMSprop: adaptive learning rate based on recent gradients
Choosing optimal learning rate is crucial - can use learning rate scheduling.""",
        
        """Time Series and Recurrent Neural Networks:
Time series data has temporal dependencies between observations. Autoregressive (AR) models use past values 
to predict future. Moving averages smooth trend. Seasonality requires differencing or seasonal decomposition. 
Recurrent Neural Networks (RNNs) process sequences with hidden state carrying information:
- LSTM (Long Short-Term Memory): gating mechanism prevents vanishing gradients for long sequences
- GRU (Gated Recurrent Unit): simplified LSTM with fewer parameters
- Attention mechanisms: model can focus on relevant parts of input
Applications: forecasting stock prices, weather prediction, language modeling, machine translation.""",
        
        """Hyperparameter Tuning Strategies:
Hyperparameters control learning (learning rate, batch size, epochs), model structure (layers, units), 
and regularization (dropout rate, L1/L2 penalty). Grid search exhaustively tries all combinations - computationally 
expensive. Random search samples randomly - often more efficient. Bayesian Optimization uses previous trials to 
guide next sampling. Early stopping monitors validation performance and stops when no improvement. 
Cross-validation assesses hyperparameter generalization. Domain knowledge and intuition guide initial ranges."""
    ]
    
    try:
        rag_service.ingest_knowledge("ml-engineer", ml_knowledge)
        logger.info("✓ ML Engineer knowledge base ingested successfully\n")
    except Exception as e:
        logger.error(f"✗ Failed to ingest ML knowledge: {str(e)}\n")
        raise


def ingest_backend_knowledge():
    """Ingest Backend-specific knowledge base"""
    
    logger.info("=" * 80)
    logger.info("INGESTING BACKEND ENGINEER KNOWLEDGE BASE")
    logger.info("=" * 80)
    
    rag_service = RAGService()
    
    backend_knowledge = [
        """REST API Design Principles:
REST (Representational State Transfer) uses HTTP for web services. Key concepts:
- Resources: entities managed by API (users, posts, products)
- HTTP Methods: GET (retrieve), POST (create), PUT (update), DELETE (remove), PATCH (partial update)
- Status Codes: 2xx success (200 OK, 201 Created), 3xx redirect, 4xx client error (400 Bad Request, 
404 Not Found, 401 Unauthorized), 5xx server error (500 Internal Server Error)
- Headers: Content-Type, Authorization, Accept, CORS headers
- Versioning: use /v1/ or Accept header for backwards compatibility
- Statelessness: each request contains all needed information, no server-side sessions
- Pagination: limit and offset for large result sets
- Error responses: consistent format with error codes and messages""",
        
        """Database Design and Normalization:
Database design organizes data to minimize redundancy and maintain consistency. Normalization levels:
- 1NF: Atomic values, no repeating groups
- 2NF: 1NF + no partial dependencies on primary key
- 3NF: 2NF + no transitive dependencies
Denormalization adds redundancy to improve query performance. Foreign keys enforce referential integrity. 
ACID properties ensure reliability:
- Atomicity: transaction succeeds or fails completely
- Consistency: data remains valid according to constraints
- Isolation: concurrent transactions don't interfere
- Durability: committed data persists after failures
Indexes on frequently queried columns speed up queries but slow writes. Query optimization uses EXPLAIN PLAN 
to identify slow queries and index bottlenecks.""",
        
        """Microservices Architecture:
Microservices break applications into small, independent services each handling specific business capability. 
Advantages: independent scaling, deployment, technology choices, and team organization. Challenges: distributed 
systems complexity, data consistency, network latency. Service discovery allows services to find each other 
dynamically. API Gateway routes client requests to appropriate services. Communication:
- Synchronous: REST APIs, gRPC for low latency
- Asynchronous: message queues (RabbitMQ, Kafka) for eventual consistency
Service boundaries should align with business domains (Domain-Driven Design). Database per service prevents 
tight coupling. Trade-off between flexibility and operational complexity.""",
        
        """Caching Strategies and Patterns:
Caching stores frequently accessed data in fast memory (Redis, Memcached) to reduce database load and latency. 
Strategies:
- Cache-aside: application checks cache first, loads from database on miss, updates cache
- Write-through: write to cache and database together - ensures consistency but slows writes
- Write-behind: write to cache first, asynchronously to database - fast but risk of data loss
Cache invalidation is notoriously difficult - options:
- Time-based (TTL): automatically expire after time interval
- Event-based: invalidate when data changes
- Manual: explicitly remove cache entries
- Versioning: version cache keys to invalidate all old versions
Cache warming pre-loads frequently needed data. Cache patterns: caching query results, session data, 
computed values. Monitor hit rates to validate cache effectiveness.""",
        
        """Horizontal Scaling and Load Balancing:
Horizontal scaling adds more servers to distribute load. Load balancing distributes requests:
- Round-robin: cycles through servers sequentially
- Least connections: sends to server with fewest active connections
- IP hash: consistent routing based on client IP
Stateless applications can be scaled horizontally - each server handles complete request. Session state 
requires: sticky sessions (route to same server), centralized storage (Redis), or client-side cookies. 
Database scaling: read replicas handle queries, writes go to primary, replication lag requires eventual consistency. 
Sharding partitions data across multiple databases by key (user ID, geographical region). Service mesh manages 
inter-service communication, retries, and timeouts.""",
        
        """Authentication and Authorization:
Authentication verifies user identity - who are you? Common methods:
- Basic auth: username/password in HTTP header (use HTTPS)
- API Keys: unique token for service-to-service auth
- JWT (JSON Web Tokens): self-contained token with claims, verified via signature
- OAuth 2.0: delegated authorization, third-party sign-in (Google, GitHub)
- LDAP: enterprise directory service integration
Authorization determines permissions - what can you do?
- Role-based access control (RBAC): users have roles with permissions
- Attribute-based access control (ABAC): fine-grained rules on attributes
- API scopes: OAuth scope limits capabilities
Security best practices:
- HTTPS encryption for all sensitive data
- Password hashing: bcrypt, argon2 (never store plaintext)
- Rate limiting: prevent brute force and abuse
- Input validation: sanitize all user input
- CORS: restrict cross-origin requests
- Security headers: CSP, X-Frame-Options, HSTS""",
        
        """Message Queues and Asynchronous Processing:
Message queues enable asynchronous communication between services. Producer sends messages, broker stores, 
consumers process. Advantages: decoupling, scalability, reliability, replay capability. 
Popular systems:
- RabbitMQ: reliable AMQP broker with routing, acknowledgments
- Apache Kafka: distributed streaming platform, high throughput, retention
- AWS SQS: managed queue service with dead-letter queues
- Redis Streams: append-only log for event streaming
Patterns:
- Work queue: distribute jobs across workers
- Pub/Sub: broadcast messages to multiple subscribers
- Event sourcing: store all state changes as events
- CQRS: separate read and write models
Dead-letter queues handle failed messages. Message ordering and exactly-once delivery have trade-offs.""",
        
        """Containerization with Docker and Kubernetes:
Docker containers package application with dependencies (libraries, runtime, OS) for consistent deployment. 
Dockerfile defines build steps. Docker Compose orchestrates multi-container local development. Benefits:
- Reproducibility: runs same everywhere
- Isolation: doesn't interfere with host system
- Efficiency: lighter weight than VMs
Kubernetes orchestrates containers in production:
- Pods: smallest deployable unit with one/multiple containers
- Services: expose pods as stable network endpoint
- Deployments: manage replica sets, rolling updates
- StatefulSets: for stateful applications requiring stable identity
- Persistent Volumes: storage for data that survives pod restarts
- Namespaces: logical cluster partitioning
- ConfigMaps/Secrets: configuration and sensitive data management
Kubernetes handles: scheduling, auto-scaling, self-healing, rolling updates.""",
        
        """Monitoring, Logging, and Observability:
Monitoring tracks system health and performance. Metrics: CPU, memory, request latency, error rates. 
Logging captures detailed events for debugging. Structured logging (JSON) enables searching. 
Distributed tracing tracks requests across services. The three pillars:
- Metrics: quantitative performance data, time-series database (Prometheus, InfluxDB)
- Logs: detailed event records, stored in ELK Stack or cloud logging
- Traces: request flow across services (Jaeger, Zipkin)
Alerts notify on anomalies or threshold violations. Dashboards visualize real-time status. 
Log aggregation centralizes logs from multiple services. Sampling high-volume metrics/traces reduces cost. 
APM (Application Performance Monitoring) identifies performance bottlenecks. Error tracking captures exceptions.""",
        
        """Deployment Strategies and CI/CD:
Continuous Integration: merge code frequently, automated tests catch issues early. 
Continuous Deployment: automatic release to production after tests pass.
Deployment strategies:
- Blue-Green: run two identical environments, switch traffic after validation
- Canary: gradually route traffic to new version, monitor for issues
- Rolling: progressively replace old instances with new, maintain availability
- Feature flags: toggle features without deployment
Infrastructure as Code (IaC): define infrastructure in version control (Terraform, CloudFormation)
CI/CD tools: Jenkins, GitLab CI, GitHub Actions, CircleCI
Pipeline stages: build, test, security scan, deploy to staging, deploy to production
Automated rollback recovers from deployment issues.""",
        
        """System Design Interview Approach:
Define requirements: functional (what system does), non-functional (scale, availability, latency, consistency)
Estimate scale: requests per second, data volume, concurrent users
Design APIs: methods, request/response formats, error handling
Database selection: SQL for structured, NoSQL for flexibility, in-memory for caching
Partitioning/sharding: distribute data and load
Caching layers: reduce database hits
Asynchronous processing: message queues for slow operations
Load balancing and redundancy: handle failures
Monitoring and logging: operational visibility
Consider trade-offs: consistency vs availability (CAP theorem), latency vs cost
Discuss bottlenecks and improvements: what would you optimize next"""
    ]
    
    try:
        rag_service.ingest_knowledge("backend-engineer", backend_knowledge)
        logger.info("✓ Backend Engineer knowledge base ingested successfully\n")
    except Exception as e:
        logger.error(f"✗ Failed to ingest Backend knowledge: {str(e)}\n")
        raise


def ingest_data_science_knowledge():
    """Ingest Data Science-specific knowledge base"""
    
    logger.info("=" * 80)
    logger.info("INGESTING DATA SCIENTIST KNOWLEDGE BASE")
    logger.info("=" * 80)
    
    rag_service = RAGService()
    
    data_science_knowledge = [
        """Exploratory Data Analysis (EDA):
EDA understands data before modeling. Techniques:
- Summary statistics: mean, median, std dev, min, max, quartiles
- Distributions: histograms, density plots identify skewness, outliers
- Correlation analysis: heatmaps show relationships between variables
- Missing values: identify patterns, decide on imputation or removal
- Outlier detection: identify and handle extreme values
- Data quality: check for duplicates, typos, encoding issues
Visualizations: scatter plots (relationships), box plots (distributions), time series plots
Understand domain and data collection process to identify biases or anomalies.""",
        
        """Statistical Hypothesis Testing:
Hypothesis testing determines if observed data supports a theory. Process:
- Null hypothesis H0: no effect or difference
- Alternative hypothesis H1: effect or difference exists
- Test statistic: computed from sample data
- P-value: probability of observing data if H0 true
- Significance level α (usually 0.05): reject H0 if p-value < α
Common tests:
- T-test: compares means of two groups
- Chi-square: categorical data association
- ANOVA: compares means across multiple groups
- Correlation tests: assess relationship strength
Common pitfalls: p-hacking (multiple tests), small sample size, confounding variables
Multiple comparison correction (Bonferroni) when conducting many tests.""",
        
        """Data Preprocessing and Handling Missing Data:
Missing data mechanisms:
- MCAR (Missing Completely At Random): no pattern, safe to ignore
- MAR (Missing At Random): missingness depends on observed data
- MNAR (Missing Not At Random): missingness depends on unobserved data
Handling strategies:
- Deletion: remove rows/columns with missing values
- Mean/median imputation: fill with central tendency
- Forward fill: copy previous value (time series)
- Model-based: predict from other features
- Multiple imputation: create multiple complete datasets
Handling outliers: remove, transform (log), or treat separately
Feature scaling: normalization (0-1) or standardization (mean=0, std=1) for distance-based algorithms
Categorical encoding: one-hot for tree models, ordinal if natural order exists""",
        
        """Feature Selection and Dimensionality Reduction:
High dimensions increase overfitting risk and computational cost. Feature selection:
- Univariate methods: select based on statistical tests with target
- Model-based: use feature importance from tree models
- RFE (Recursive Feature Elimination): iteratively remove least important
Dimensionality reduction:
- PCA: linear combination of features capturing maximum variance
- t-SNE: non-linear for visualization
- Autoencoder: neural network learns compressed representation
Feature engineering: create new features from raw data
Curse of dimensionality: many features need exponentially more data to avoid overfitting""",
        
        """Regression and Classification Models:
Regression predicts continuous values:
- Linear regression: simple, interpretable, assumes linearity
- Polynomial regression: captures non-linear relationships
- Ridge/Lasso: regularized linear regression preventing overfitting
- SVR: support vector regression for non-linear boundaries
- Tree-based: Random Forest, Gradient Boosting
Classification predicts categorical values:
- Logistic regression: binary/multi-class, probabilistic
- Naive Bayes: assumes feature independence, efficient
- Decision trees: interpretable, prone to overfitting
- Random Forest: ensemble of trees, robust
- SVM: finds maximum margin boundary
- Neural networks: flexible, requires more data
Model choice depends on interpretability needs, data size, feature types""",
    ]
    
    try:
        rag_service.ingest_knowledge("data-scientist", data_science_knowledge)
        logger.info("✓ Data Scientist knowledge base ingested successfully\n")
    except Exception as e:
        logger.error(f"✗ Failed to ingest Data Science knowledge: {str(e)}\n")
        raise


if __name__ == "__main__":
    try:
        logger.info("\n🔄 Starting Knowledge Base Ingestion...\n")
        
        # Ingest all role-specific knowledge bases
        ingest_ml_knowledge()
        ingest_backend_knowledge()
        ingest_data_science_knowledge()
        
        logger.info("=" * 80)
        logger.info("✓ ALL KNOWLEDGE BASES INGESTED SUCCESSFULLY!")
        logger.info("=" * 80)
        logger.info("\nYou can now start the application with: python -m uvicorn app.main:app --reload")
        logger.info("API documentation will be available at: http://localhost:8000/docs\n")
        
    except Exception as e:
        logger.error(f"\n✗ Failed to ingest knowledge bases: {str(e)}")
        logger.error("Please check your setup and try again.")
        sys.exit(1)
